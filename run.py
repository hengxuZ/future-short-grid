# -*- coding: utf-8 -*-
from app.BinanceAPI import BinanceAPI
from app.authorization import api_key,api_secret
from data.runBetData import RunBetData
from app.dingding import Message
from data.calcIndex import CalcIndex
import time

binan = BinanceAPI(api_key,api_secret)
runbet = RunBetData()
msg = Message()
index = CalcIndex()
class Run_Main():

    def __init__(self):
        self.coinList = runbet.get_coinList()
        # self.coinType = runbet.get_cointype()  # 交易币种
        # self.profitRatio = runbet.get_profit_ratio() # 止盈比率
        # self.doubleThrowRatio = runbet.get_double_throw_ratio() # 补仓比率
        pass

    def pre_data(self,cointype):
        future_buy_price = runbet.get_future_buy_price(cointype)  # 现货买入价格
        future_sell_price = runbet.get_future_sell_price(cointype)  # 现货卖出价格
        future_quantity = runbet.get_future_quantity(cointype)  # 期货买入量
        future_step = runbet.get_future_step(cointype)  # 当前期货步数(手数)

        cur_market_price = binan.get_ticker_price(cointype)  # 当前交易对市价
        right_size = len(str(cur_market_price).split(".")[1])
        return [future_buy_price,future_sell_price,future_quantity,future_step,cur_market_price,right_size]

    def loop_run(self):
        while True:
            for coinType in self.coinList:
                [future_buy_price,future_sell_price,future_quantity,future_step,cur_market_price,right_size] = self.pre_data(coinType)

                # 开空
                if future_buy_price <= cur_market_price and index.calcAngle(coinType, "5m",True,right_size):  # 是否满足开仓价

                    future_res = msg.open_sell_market_msg(coinType, future_quantity)  # 期货买入开空
                    if future_res['orderId']:
                        time.sleep(1)
                        runbet.set_ratio(coinType)
                        runbet.set_record_price(coinType,cur_market_price) # 记录买入价格
                        runbet.modify_future_price(coinType,cur_market_price,future_step + 1)  # 修改data.json中价格
                        # runbet.set_future_step(coinType,)
                        time.sleep(60 * 1)  # 挂单后，停止运行1分钟
                    else:
                        break

                # 平空
                elif future_sell_price >= cur_market_price and index.calcAngle(coinType, "5m", False,right_size):  # 是否满足卖出价

                    if future_step > 0:
                        future_res = msg.do_sell_market_msg(coinType, runbet.get_future_quantity(coinType,False))  # 期货卖出开多
                        if future_res['orderId']:
                            runbet.set_ratio(coinType)
                            runbet.modify_future_price(coinType,runbet.get_record_price(coinType),future_step - 1)  # 修改data.json中价格

                            time.sleep(60 * 0.5)  # 挂单后，停止运行1分钟
                        else:
                            break
                    else:
                        runbet.modify_future_price(cur_market_price)

                time.sleep(2) # 为了不被币安api请求次数限制


# if __name__ == "__main__":
#     instance = Run_Main()
#     try:
#         instance.loop_run()
#     except Exception as e:
#         error_info = "报警：开空网格服务停止.错误原因{info}".format(info=str(e))
#         msg.dingding_warn(error_info)


#调试看报错运行下面，正式运行用上面
if __name__ == "__main__":

    # instance = Run_Main()
    # instance.loop_run()
    print(runbet.get_record_price("EOSUSDT"))

