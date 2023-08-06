import json
import pandas as pd


# 导入常用的固定路径(多平台通用)
from kw618._file_path import *
# 本脚本依赖很多 utils_requests的函数和模块, 直接用*  (注意要避免循环导入问题)
from kw618.k_requests.utils_requests import *
from kw618.k_requests.ocr import *
from kw618.k_python.utils_python import *
from kw618.k_pandas.utils_pandas import *

from kw618.k_finance.utils_quant import *
from kw618.k_finance.const import ulist_change_name_dict

req = myRequest().req
client = pymongo.MongoClient(f'mongodb://kerwin:kw618@{HOST}:27017/')
db_for_quant = client["quant"]




# 原始模型类
class OrgModel():
    # """
    #     hc模型中, 暂时只允许每次只hc一个stock;
    #     跑sp的时候, 只要给每个stock一定的初始cash_balance即可
    # """

    def __init__(self, stock_code="", Zqdm="", init_cash_balance=100000):
        """
            params:
                init_cash_balance: 初始账户余额

            notice:
                1. 初始化时, Zqdm和stock_code 二选其一, 就可以实现初始化.

        """
        # 1. 初始化'静态'数据
        self.init_cash_balance = init_cash_balance # 记录一个初始启动资金(固定)
        self.cash_balance = self.init_cash_balance # 后面动态更新的余额
        if stock_code:
            self.stock_code = stock_code
            self.Zqdm = Q._StockCode_to_Zqdm(stock_code_lst=[self.stock_code])[0]
        elif Zqdm:
            self.Zqdm = Zqdm
            self.stock_code = Q._Zqdm_to_StockCode(Zqdm_lst=[self.Zqdm])[0]
        else:
            raise Exception("代码输入错误, 初始化未成功!!\n")
        self.Zqmc = Q._Zqdm_to_Zqmc(Zqdm_lst=[self.Zqdm])[0]
        self.f1 = Q._Zqdm_to_f1(Zqdm_lst=[self.Zqdm])[0] # 2:A股; 3:ETF基金;  (后期可用于计算交易费的佣金差异)
        self.sxf_rate = 0.00018 # 手续费率按'万1.8'来计算
        self.ETF_fee_rate = 0.006/365 # 托管费率按 '一年千6' 来计算 (托管费每日计提, 无需在每笔交易中另行支付) (貌似只有在及哦啊一日才会生成)

        # 2. 读取mongo中的历史'日K'数据的df
            # (每个实例都需要获取新的'日K'数据) (后面跑策略依赖这里的'日K'数据!!)
        whole_hist_df = read_mongo(db_for_quant["hist_allstock"], {"stock_code":self.stock_code})

        # 3. 数据预处理 (得到双均线的差值)
        # whole_hist_df["_num"] = np.arange(1, len(whole_hist_df)+1) # 新建一个'顺序序列' (但是需要在init_data函数中操作此步骤)
        whole_hist_df["5v30"] = whole_hist_df["5d_avg"] - whole_hist_df["30d_avg"]
        whole_hist_df["5v20"] = whole_hist_df["5d_avg"] - whole_hist_df["20d_avg"]
        whole_hist_df["5v10"] = whole_hist_df["5d_avg"] - whole_hist_df["10d_avg"]
        whole_hist_df["10v30"] = whole_hist_df["10d_avg"] - whole_hist_df["30d_avg"]
        self.whole_hist_df = whole_hist_df # 所有完整的历史数据
        self.launch_date = self.whole_hist_df.iloc[0]["market_date"] # 上市日期

        # 4. 初始化'动态'数据
        self.init_data()


    def init_data(self, selected_days=99999, start_date=None, end_date=None, pt=False):
        """
            function: 用于后面重复执行run方法时候使用的'初始化'方法 (区别于__init__)
                    步骤:
                        1. 筛选回测日期
                        2. 初始化'通用型变量'
                        3. 执行'do_every_evening'的汇总函数
                        4. 初始化'针对型变量'
            params:
                selected_days: 筛选的天数  (99999代表: 取所有日期)
        """

        # 1. 筛选回测日期 (得到query_set)
            # i. 若给了一个start_date和一个selected_days: 从开始日期向后取xx天
            # ii. 若给了一个end_date和一个selected_days: 从截止日期向前取xx天
        if start_date is not None:
            if end_date:
                pass
            else:
                end_date = get_later_date(start_date, f"{selected_days} days")
        elif start_date is None:
            if end_date:
                start_date = get_previous_date(end_date, f"{selected_days} days")
            else:
                end_date = get_today_date()
                start_date = get_previous_date(end_date, f"{selected_days} days")
            # 如果开始日期早于'上市日期', 则把'上市日期'作为'开始日期'
        if start_date < self.launch_date:
            start_date = self.launch_date # 覆盖它
            # 如果结束日期晚于'今天最新日期', 则把'今天日期'作为'结束日期'
        if end_date > get_today_date():
            end_date = get_today_date() # 覆盖它
        query_set = f"'{start_date}' <= market_date <= '{end_date}'"
        self.hist_df = self.whole_hist_df.query(query_set)
        self.hist_df["_num"] = np.arange(1, len(self.hist_df)+1) # 新建一个'顺序序列'
        self.selected_days = get_delta_days(start_date=start_date, end_date=end_date)
        self.start_date = start_date
        self.end_date = end_date

        # 2. 初始化'通用型变量':
            # 1. 现金流&开平仓数流
                # (有方向): 历次buying&selling的价格/股数
                # 负数:表示买入该stock; 正数:表示卖出该stock (因为最终统计的是现金的剩余量)
        self.cash_flow_lst = []
        self.deal_count_flag = []
            # 4. 持仓股票数
        self.chicang_stock_count = 0
            # 5. 平均成本价
        self.avg_cost_price = 0
        self.cost_market_value = 0
        self.market_value_percentage = 0
        self.market_value_percentage_lst = []
            # 6. 初始化余额 [临时]
        self.cash_balance = self.init_cash_balance
            # 7. 交易次数
        self.buy_times = 0
        self.sell_times = 0
        self.buy_day_lst = []
        self.sell_day_lst = []
                # 2. 每次交易操作时, 距离上次操作的天数 (不管是买,还是卖)
        self.deal_day_lst = []
            # 8. 是否打印(必要的节点信息)
        self.pt = pt
            # 9. 盈亏比例
        self.LjYkbl = np.nan
        self.DrYkbl = np.nan
            # 11. 更新价格
                # 截取到的时间段内最新一天的价格
        if len(self.hist_df) > 0:
            self.newest_date = self.hist_df.iloc[-1]["market_date"]
            self.newest_price = self.hist_df.iloc[-1]["end_price"]
            # self.newest_price = Q.req_newest_data([self.stock_code])["NewestPrice"].iloc[0]
                    # 暂时用'newest_price'替代 (后续策略计算时, 需要用当天价格覆盖它)
            self.today_date = self.newest_date
            self.today_price = self.newest_price

        #     # 12. 持仓股若卖出需要多少手续费?  # 已经放在 do_every_evening中了
        # self.chicang_stock_deal_fee = 0
        self.ETF_today_fee = 0
        self.ETF_fee_lst = []
        self.ETF_total_fee = 0

        # 3. 执行'do_every_evening'的汇总函数:
        self.do_every_evening()

        # 4. 初始化'针对型变量':
            # 具体策略中需要用到的初始化变量
            # 1. 双均线策略:
                # 上一天的'长短线差值'
        self.last_diff_score = np.nan

            # 2. 止损策略:
                # 累计涨幅:
                    # 用于计算每天的累计涨幅 (是市场的实盘涨幅, 与上面LjYkbl的个人涨幅无关)
                    # (每天append进'最新的累计涨幅')
                # 1. "市场"累计盈亏
        self.MarketLjYk = 0.0  # 这是指"市场上"的"累计盈亏" (区别于: "自己账户"的"LjYk")
        self.MarketLjYkbl = 0.0  # 这是指"市场上"的"累计盈亏比例" (区别于: "自己账户"的"LjYkbl")
        self.MarketLjYk_lst = []
        self.MarketLjYkbl_lst = []
                # 2. "个人"累计盈亏
        self.MyLjYk = 0.0  # 这是指"个人账户"的"累计盈亏" (区别于: "市场"的"LjYk")
        self.MyLjYkbl = 0.0  # 这是指"个人账户"的"累计盈亏比例" (区别于: "市场"的"LjYkbl")
        self.MyLjYk_lst = []
        self.MyLjYkbl_lst = []







    def do_every_morning(self, doc):
        """
            function: 每天早上记录必要的数据
                    (因为不管哪个策略都需要有这一步, 所以把它抽离出来)

            params:
                doc: apply函数中的doc  (也就是self.hist_df中的每一行)


        """

        # 1. 记录 "当天" 的 "日K" 数据
        self.today_date = doc.get("market_date") # 每天实时更新'最新价格'
        self.today_price = doc.get("end_price")
        self.today_days = doc.get("_num") # 得到今天距离'基准日期'的天数
        self.DrYkbl = round(doc.get("growth_rate"), 4) # 每天实时更新'当日盈亏比例'
        self.DrYk = round(doc.get("growth_amount"), 4) # 每天实时更新'当日盈亏'
        if np.isnan(self.DrYkbl) == True: # 如果DrYkbl是空值, 默认用0来填充
            self.DrYkbl = 0.0
        if np.isnan(self.DrYk) == True: # 如果DrYkbl是空值, 默认用0来填充
            self.DrYk = 0.0
        print(self.today_date, self.today_days, self.today_price, self.DrYkbl, self.DrYk)

        # 2. 记录"市场上"的累计数据
        self.MarketLjYk += self.DrYk # 每天累加
        self.MarketLjYkbl += self.DrYkbl # 每天累加
        self.MarketLjYk = round(self.MarketLjYk, 4)
        self.MarketLjYkbl = round(self.MarketLjYkbl, 4)
        self.MarketLjYk_lst.append(self.MarketLjYk)
        self.MarketLjYkbl_lst.append(self.MarketLjYkbl)
        print(self.MarketLjYk, self.MarketLjYkbl)

        # 3. 记录"个人账户"的累计数据
        if self.avg_cost_price != 0:
            self.MyLjYk = round(self.today_price - self.avg_cost_price, 4) # 个人账户的'累计盈亏'的计算方式: 直接用 "最新价格 - 成本均价"
            self.MyLjYkbl = round(self.MyLjYk / self.avg_cost_price, 4)
        elif self.avg_cost_price == 0:
            self.MyLjYk = 0.0
            self.MyLjYkbl = 0.0
        self.MyLjYk_lst.append(self.MyLjYk)
        self.MyLjYkbl_lst.append(self.MyLjYkbl)
        print(self.MyLjYk, self.MyLjYkbl)

        print("\n\n")


    def do_every_evening(self):
        """
            function: 每天晚上记录必要的数据 (一般是受今日交易数据所影响的数据)
                        (相当于对今天数据的汇总)

            params:
                无: 不依赖于doc, 所以也可以放在 init_data()方法 中执行


        """

        # 1. 计算当前持仓股票的'成本市值'
            # 成本市值: 指持有的这些股票共'花了多少钱','最新市值'要大于它才算有利润!
        self.cost_market_value = self.chicang_stock_count * self.avg_cost_price
        # 2. 计算当前持仓股票的'今日市值'
            # i. A股直接相乘就是'今日市值'
        self.today_market_value = self.chicang_stock_count * self.today_price
            # ii. ETF需要在'今日市值'中计提每日的管托费
        if self.f1 == 3:
            self.ETF_today_fee = self.today_market_value * self.ETF_fee_rate
            self.ETF_fee_lst.append(self.ETF_today_fee)
            self.ETF_today_fee = sum(self.ETF_fee_lst)
            self.today_market_value -= self.ETF_total_fee

        # 3. 现金流汇总
        self.sum_cash_flow = sum(self.cash_flow_lst)
        # 4. 开平仓数流汇总
        self.sum_deal_count_flag = sum(self.deal_count_flag)
            # 持有A股, 如果要卖出的话, 需要多少手续费? (ETF直接返回0)
        self.chicang_stock_deal_fee = self.get_commission_fee(
            Mmlb="S", deal_price=self.today_price, deal_count=abs(self.sum_deal_count_flag),
        )

        # 5. 今天的"总资产"
        self.total_capital_value = self.cash_balance + self.today_market_value
        # 6. 今天的"净资产" (已扣除今天持仓的交易成本) (即:假设今天把持有的股票全卖了, 账户总资产是多少?)
        self.net_capital_value = self.total_capital_value - self.chicang_stock_deal_fee
        # 7. 今天的"市值占比"
        self.market_value_percentage = self.today_market_value / self.total_capital_value
        self.market_value_percentage_lst.append(self.market_value_percentage)



    def get_commission_fee(self, Mmlb, deal_price, deal_count):
        """
            params:
                Mmlb: 买卖类别  # "B" / "S"
                deal_price: 交易单价 (一股的价格)
                deal_count: 交易数量
        """

        if deal_count > 0:
            # 会产生手续费
                # 1. A股的手续费
            if self.f1 == 2:
                sxf = max(self.sxf_rate*(deal_price*deal_count), 5.0)

                if Mmlb == "B":
                    total_fee = sxf
                elif Mmlb == "S":
                    yhs = 0.001*(deal_price*deal_count) # 印花税都是'千分之一'的
                    sxf = 5.0
                    total_fee = yhs + sxf

                return total_fee

                # 2. ETF的手续费
            elif self.f1 == 3:
                return 0 # ETF的托管费是'每日计提'的, 所以不再在每笔交易中另外产生
        else:
            return 0


    def buying(self, buying_price, buying_count):
        # 1. 得到真实的所有'买入成本' (包含所有手续费)
        buying_count = buying_count // 100 * 100
        commission_fee = self.get_commission_fee(
            Mmlb="B", deal_price=buying_price, deal_count=buying_count,
        )
        all_buying_cost = buying_price*buying_count + commission_fee # 真实股票市值成本 = 股票成本市值 + 所有的交易手续费

        # 2. [暂时策略]: 账户余额<待购入股票金额, 不断尝试缩小购买量 (尝试3次)
        if self.cash_balance < all_buying_cost:
            for _ in range(3):
                buying_count = int(buying_count *0.98) # 这个0.98可以自定义调整
                all_buying_cost = buying_price*buying_count + commission_fee # 真实股票市值成本 = 股票成本市值 + 所有的交易手续费
                if self.cash_balance >= all_buying_cost:
                    break # 当不断缩小购买量后, 一旦余额足够支付, 则退出循环


        # 3. 只有当现金余额>=待购入股票金额, 才能真的执行'买的操作' (否则就是逻辑bug)
        if (self.cash_balance >= all_buying_cost) and (buying_count != 0):
            # 1. '现金余额'减少
            self.cash_balance -= all_buying_cost
            # 2. '持仓股数'增加
                # (old_cost_market_value 需要在'持仓数量'增加之前计算)
            old_cost_market_value = self.chicang_stock_count * self.avg_cost_price
            self.chicang_stock_count += buying_count
            # 3. '现金流'&'开平仓数流'记录
                # 1. 负现金流: 表示买入'xxx元'的stock
            self.cash_flow_lst.append(-1 * all_buying_cost)
                # 2. 负开平仓数流: 表示买入'xxx股'的stock
            self.deal_count_flag.append(-1 * buying_count)
            # 4. 每次"买入交易"都需要重新计算'平均成本价'  ('卖出交易'不影响平均成本, 只要减去'持仓数量', 计算出来的'成本市值'就会跟着减少了)
                # (成本市值的统计是'无意义'的, 都是动态的用 当前'平均成本价*持仓数量' 计算得到的)
            new_cost_market_value = all_buying_cost
            self.avg_cost_price = (old_cost_market_value + new_cost_market_value) / self.chicang_stock_count
            # 5. '买入次数' +1
            self.buy_times += 1
            # 6. '距离上次买入天数' 添加进 buy_day_lst 中
            self.buy_day_lst.append(self.today_days-sum(self.buy_day_lst))
            # 7. '距离上次交易天数' 添加进 deal_day_lst 中
            self.deal_day_lst.append(self.today_days-sum(self.deal_day_lst))
            if self.pt == True:
                print(f"[{self.today_date}] 买入股票:{buying_count}股, 成本市值:{all_buying_cost}\n", "=="*50)


    def selling(self, selling_price, selling_count):

        # 1. 得到真实的卖出后的'到手现金' (已经扣除所有手续费)
        selling_count = selling_count // 100 * 100
        commission_fee = self.get_commission_fee(
            Mmlb="S", deal_price=selling_price, deal_count=selling_count,
        )
        all_selling_cash = selling_price * selling_count - commission_fee # 到手现金 = 股票卖出价 - 所有的交易手续费

        # 2. 只有当自己的持仓股数大于你要卖的股数时, 才能真的执行'卖的操作' (否则就是逻辑bug)
        if (self.chicang_stock_count >= selling_count) and (selling_count != 0):
            # 1. '现金余额'增加
            self.cash_balance += all_selling_cash
            # 2. '持仓股数'减少
            self.chicang_stock_count -= selling_count
            # 3. '现金流'&'开平仓数流'记录
                # 1. 正现金流: 表示卖出'xxx元'的stock
            self.cash_flow_lst.append(1 * all_selling_cash)
                # 2. 正开平仓数流: 表示卖出'xxx股'的stock
            self.deal_count_flag.append(1 * selling_count)
            # 4. '卖出交易'不会影响到成本价
            pass
            # 5. '卖出次数' +1
            self.sell_times += 1
            # 6. '距离上次卖出天数' 添加进 sell_day_lst 中
            self.sell_day_lst.append(self.today_days-sum(self.sell_day_lst))
            # 7. '距离上次交易天数' 添加进 deal_day_lst 中
            self.deal_day_lst.append(self.today_days-sum(self.deal_day_lst))
            if self.pt == True:
                print(f"[{self.today_date}] 卖出股票:{selling_count}股, 到手现金:{all_selling_cash}\n", "=="*50)


    def return_asset_dict(self):

        # 1. 打印账户整体的资金状况
        if self.pt == True:
            sprint(cash_balance=self.cash_balance)
            sprint(today_market_value=self.today_market_value)
            sprint(net_capital_value=self.net_capital_value)
            print("=="*50)
            print("=="*50, "\n\n\n\n\n")

        # 2. '账户资产'相关信息
        asset_dict = {
            "net_capital_value" : self.net_capital_value,
            # "all_arg_msg" : self.all_arg_msg,
            "stock_code" : self.stock_code,
            "Zqdm" : self.Zqdm,
            # "Zqmc" : self.Zqmc,
            "selected_days" : self.selected_days,
            "launch_date" : self.launch_date,
            "start_date" : self.start_date,
            "end_date" : self.end_date,
            # "sell_day_lst" : self.sell_day_lst,
            "sell_times" : self.sell_times,
            # "cash_flow_lst" : self.cash_flow_lst,
            "sum_cash_flow" : self.sum_cash_flow,
            "cash_balance" : self.cash_balance,
            "today_market_value" : self.today_market_value,
        }

        return asset_dict


    def strategy_cal(self, doc):
        """
            function: 策略计算的主函数 (最主要的"计算模块") [apply函数]
        """
        # 1. 每早:获取必要数据
        self.do_every_morning(doc) # 每个策略都需要更新的'每日数据'

        # 2. 策略的主要内容
        # ====================================================
        # ====================================================
        #     # 1. 金叉: (昨天<0, 今天>0): 需要 buying it
        # if today_diff_score>0 and self.last_diff_score<=0:
        #     buying_count = self.cash_balance // self.today_price # [暂时设定] (待优化)
        #     self.buying(buying_price=self.today_price, buying_count=buying_count)
        #
        #     # 2. 死叉: (昨天>0, 今天<0): 需要 selling it
        # if today_diff_score<0 and self.last_diff_score>=0:
        #     selling_count = self.chicang_stock_count # 当出现死叉时, 把所有的持仓全部抛出
        #     self.selling(selling_price=self.today_price, selling_count=selling_count)

        pass # 每天都不进行任何操作

        # ====================================================
        # ====================================================


        # 3. 每晚:更新必要数据
        self.do_every_evening() # 每个策略都需要更新的'每日数据'


    def run(self, selected_days=99999, start_date=None, end_date=None, pt=False):
        """
            function: 整个'策略类'的执行入口
            params:
                selected_avg: 选择哪两根均线作为长短线的计算差值
                selected_days:
                    1. 回测的天数 (越久远的数据可能与当前的市场差异很大, 而且也伴随通货膨胀之类的影响因素)
                    2. 日期的默认选取方式: 从今天开始, 倒退几天
                    3. 这里的天数: 是指实际天数 (不是"股市的交易天数")
                start_date/end_date: 日期的str标准格式: 2020-07-20
                pt: 是否需要打印输出

            return:
                self.asset_dict (整体的收益情况) (dict类型)

        """

        # 1. 初始化数据(清零)
            # (不清零的话, 会导致重复run方法时候出错)
        self.init_data(selected_days=selected_days, start_date=start_date, end_date=end_date, pt=pt)

        # A. 当存在'该时间段内的df'时:
        if len(self.hist_df) > 0:
            self.all_arg_msg = f"【参数】==> stock_code:{self.stock_code}; days:{self.selected_days} (start:{self.start_date} -- end:{self.end_date})"
            if self.pt == True:
                print("\n\n", self.all_arg_msg, "\n")

            # 2. 执行策略计算
            self.hist_df.apply(self.strategy_cal, axis=1) # 运用上面的"策略计算"函数 (会把所有"买卖操作"数据存入 self.cash_flow_lst)

            # 3. 查看收益情况
            self.asset_dict = self.return_asset_dict() # 返回"账户资产相关信息"

            return self.asset_dict

        # B. 当不存在'该时间段内的df'时:
        else:
            return {} # 返回空dict






# 双均线策略: 回测版本
class DoubleMovingAverage(OrgModel):

    def strategy_cal(self, doc):
        """
            function: 策略计算的主函数 (最主要的"计算模块") [apply函数]
        """
        # 1. 每早:获取必要数据
        self.do_every_morning(doc) # 每个策略都需要更新的'每日数据'
        today_diff_score = doc.get(self.selected_avg) # 可以选取不同的 "长短线" (由run方法中给出)

        # 2. 策略的主要内容
        # ====================================================
        # ====================================================
            # 1. 金叉: (昨天<0, 今天>0): 需要 buying it
        if today_diff_score>0 and self.last_diff_score<=0:
            buying_count = self.cash_balance // self.today_price # [暂时设定] (待优化)
            self.buying(buying_price=self.today_price, buying_count=buying_count)

            # 2. 死叉: (昨天>0, 今天<0): 需要 selling it
        if today_diff_score<0 and self.last_diff_score>=0:
            selling_count = self.chicang_stock_count # 当出现死叉时, 把所有的持仓全部抛出
            self.selling(selling_price=self.today_price, selling_count=selling_count)

        # ====================================================
        # ====================================================


        # 3. 每晚:更新必要数据
        self.do_every_evening() # 每个策略都需要更新的'每日数据'
            # 用今日的score替换昨天的 (保证每个循环中, last_diff_score中都是昨日的数据)
        self.last_diff_score = today_diff_score






    def run(self, selected_avg="5v30", selected_days=99999, start_date=None, end_date=None, pt=False):
        """
            function: 整个'策略类'的执行入口
            params:
                selected_avg: 选择哪两根均线作为长短线的计算差值
                selected_days:
                    1. 回测的天数 (越久远的数据可能与当前的市场差异很大, 而且也伴随通货膨胀之类的影响因素)
                    2. 日期的默认选取方式: 从今天开始, 倒退几天
                    3. 这里的天数: 是指实际天数 (不是"股市的交易天数")
                start_date/end_date: 日期的str标准格式: 2020-07-20
                pt: 是否需要打印输出

            return:
                self.asset_dict (整体的收益情况) (dict类型)

        """

        # 1. 初始化数据(清零)
            # (不清零的话, 会导致重复run方法时候出错)
        self.init_data(selected_days=selected_days, start_date=start_date, end_date=end_date, pt=pt)

        # A. 当存在'该时间段内的df'时:
        if len(self.hist_df) > 0:
            self.selected_avg = selected_avg # 长短线指标选择 (几日均线与几日均线的差值)
            self.all_arg_msg = f"【参数】:stock_code:{self.stock_code}; days:{self.selected_days} (start:{self.start_date} -- end:{self.end_date})"
            if self.pt == True:
                print("\n\n", self.all_arg_msg, "\n")

            # 2. 执行策略计算
            self.hist_df.apply(self.strategy_cal, axis=1) # 运用上面的"策略计算"函数 (会把所有"买卖操作"数据存入 self.cash_flow_lst)

            # 3. 查看收益情况
            self.asset_dict = self.return_asset_dict() # 返回"账户资产相关信息"

            return self.asset_dict

        # B. 当不存在'该时间段内的df'时:
        else:
            return {} # 返回空dict







class StopLoss(OrgModel):

    def strategy_cal(self, doc):
        """
            function: 策略计算的主函数 (最主要的"计算模块") [apply函数]
        """
        # 1. 每早:获取必要数据
        self.do_every_morning(doc) # 每个策略都需要更新的'每日数据'

        # # 2. 策略的主要内容
        # # ====================================================
        # # ====================================================

        #     # 1. 金叉: (昨天<0, 今天>0): 需要 buying it
        # if today_diff_score>0 and self.last_diff_score<=0:
        #     buying_count = self.cash_balance // self.today_price # [暂时设定] (待优化)
        #     self.buying(buying_price=self.today_price, buying_count=buying_count)
        #
        #     # 2. 死叉: (昨天>0, 今天<0): 需要 selling it
        # if today_diff_score<0 and self.last_diff_score>=0:
        #     selling_count = self.chicang_stock_count # 当出现死叉时, 把所有的持仓全部抛出
        #     self.selling(selling_price=self.today_price, selling_count=selling_count)

        # TODO: 止损稳赢策略
        pass

        # # ====================================================
        # # ====================================================


        # 3. 每晚:更新必要数据
        self.do_every_evening() # 每个策略都需要更新的'每日数据'





    def run(self, first_percentage=0.03, stoploss_rate=0.05, selected_days=100, start_date=None, end_date=None, pt=True):
        """
            function: 整个'策略类'的执行入口
            params:
                selected_avg: 选择哪两根均线作为长短线的计算差值
                selected_days:
                    1. 回测的天数 (越久远的数据可能与当前的市场差异很大, 而且也伴随通货膨胀之类的影响因素)
                    2. 日期的默认选取方式: 从今天开始, 倒退几天
                    3. 这里的天数: 是指实际天数 (不是"股市的交易天数")
                start_date/end_date: 日期的str标准格式: 2020-07-20
                pt: 是否需要打印输出

            return:
                self.asset_dict (整体的收益情况) (dict类型)

        """

        # 1. 初始化数据(清零)
            # (不清零的话, 会导致重复run方法时候出错)
        self.init_data(selected_days=selected_days, start_date=start_date, end_date=end_date, pt=pt)

        # A. 当存在'该时间段内的df'时:
        if len(self.hist_df) > 0:
            # self.selected_avg = selected_avg # 长短线指标选择 (几日均线与几日均线的差值)
            # self.all_arg_msg = f"【参数】:stock_code:{self.stock_code}; days:{self.selected_days} (start:{self.start_date} -- end:{self.end_date})"
            # if self.pt == True:
            #     print("\n\n", self.all_arg_msg, "\n")

            # 2. 执行策略计算
            self.hist_df.apply(self.strategy_cal, axis=1) # 运用上面的"策略计算"函数 (会把所有"买卖操作"数据存入 self.cash_flow_lst)

            # 3. 查看收益情况
            self.asset_dict = self.return_asset_dict() # 返回"账户资产相关信息"

            return self.asset_dict

        # B. 当不存在'该时间段内的df'时:
        else:
            return {} # 返回空dict


















def main():
    o = OrgModel(Zqdm="002505")
    d = o.run(30)

    o = DoubleMovingAverage("0.159995", init_cash_balance=100000)
    asset_dict = o.run(selected_days=30, selected_avg="5v10")
    print(asset_dict)







if __name__ == '__main__':
    print("Start test!\n\n")
    main()
    print("\n\n\nIt's over!")
