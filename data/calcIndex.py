from app.BinanceAPI import BinanceAPI
from app.authorization import api_key,api_secret
from app.dingding import Message
from data.runBetData import RunBetData
import os,json,time
runbet = RunBetData()
binan = BinanceAPI(api_key,api_secret)
msg = Message()

class CalcIndex:

    def __init__(self):
        # self.coinType = runbet.get_cointype()  # 交易币种
        pass

    def calcMA(self,symbol,interval,point):
        '''
        :param symbol: 交易对
        :param interval: 间隔时间 1h 4h 1d
        :return: 当前时间ma20 40 60 120 的值
        '''
        sum_ma10=0
        sum_ma20=0
        sum_ma40=0
        sum_ma60 = 0
        sum_ma120 = 0

        num = 0
        data = binan.get_klines(symbol, interval, 120)
        for i in range(len(data)):
            if i>=110 and i <=120:
                sum_ma10 += float(data[i][4])
            if i>=100 and i <=120:
                sum_ma20 += float(data[i][4])
            if i>=80 and i <=120:
                sum_ma40 += float(data[i][4])
            if i >= 60 and i <= 120:
               sum_ma60 += float(data[i][4])

            sum_ma120 +=float(data[i][4])
        return [round(sum_ma10/10,point),round(sum_ma20/20,point),round(sum_ma40/40,point),round(sum_ma60/60,point), round(sum_ma120/120,point)]


    def calcTotal(self,arr,step):
        total = 0
        for i in range(step):
            if len(arr) <= i:
                total += arr[-1]
            else:
                total += arr[i]
        return total

    def calcSlopeMA10(self,symbol,interval,point):
        '''

        :param symbol:
        :param interval:
        :return: 上一时刻的m20值
        '''
        last_ma10 = 0
        next_ma10 = 0
        num = 0
        data = binan.get_klines(symbol, interval, 11)
        for i in range(len(data)):
            if i==0:
                last_ma10+=float(data[i][4])
            elif i==10:
                next_ma10+=float(data[i][4])
            else:
                last_ma10+=float(data[i][4])
                next_ma10+=float(data[i][4])

        return [round(last_ma10/10,point),round(next_ma10/10,point)]

    def calcSlopeMA5(self,symbol,interval,point):
        '''

        :param symbol:
        :param interval:
        :return: 上一时刻的m20值
        '''
        last_ma5 = 0
        next_ma5 = 0
        data = binan.get_klines(symbol, interval, 6)
        for i in range(len(data)):
            if i==0:
                last_ma5+=float(data[i][4])
            elif i==5:
                next_ma5+=float(data[i][4])
            else:
                last_ma5+=float(data[i][4])
                next_ma5+=float(data[i][4])

        return [round(last_ma5/5,point), round(next_ma5/5,point)]


    # def calcSlope(self,symbol,interval,direction):
    #     '''
    #
    #     :param symbol:
    #     :param interval:
    #     :param direction: 多头还是空头 多:true 空为:false
    #     :return: 斜率是否满足开仓
    #     '''
    #     lastMA10,tmpMA10 = self.calcSlopeMA10(symbol,interval)
    #     if direction:
    #         return tmpMA10 > lastMA10
    #     else:
    #         return lastMA10 > tmpMA10


    def calcAngle(self,symbol,interval,direction,point):
        '''

        :param symbol:
        :param interval:
        :param direction:
        :return: 趋势来了 正在拉伸 不买
        '''
        lastMA5,tmpMA5 = self.calcSlopeMA5(symbol, interval,point)
        if direction:
            return tmpMA5 <= lastMA5
        else:
            return tmpMA5 >= lastMA5

    def calcMA10(self,symbol,interval,point):
        sum_ma10 = 0
        data = binan.get_klines(symbol, interval, 10)
        for i in range(len(data)):
            sum_ma10+=float(data[i][4])

        return round(sum_ma10 / 10,point)

    def get_position_price(self,direction=True):
        tmp = binan.get_positionInfo(runbet.get_cointype())
        for item in tmp:  # 遍历是有仓位
            if direction: # 多头持仓均价
                if item['positionSide'] == "LONG" and float(item['positionAmt']) != 0.0:
                    return float(item['entryPrice'])
            else:        # 空头持仓均价
                if item['positionSide'] == "SHORT" and float(item['positionAmt']) != 0.0:
                    return float(item['entryPrice'])

        return False