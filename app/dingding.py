# author-wechat：findpanpan

import requests,json

# windows
# from app.authorization import dingding_token, recv_window,api_secret,api_key
# from app.BinanceAPI import BinanceAPI
# linux
from app.BinanceAPI import BinanceAPI
from app.authorization import dingding_token, recv_window,api_secret,api_key

class Message:

    def do_buy_limit_msg(self,market, quantity, price, profit_usdt=0):
        '''
        合约开多，带有钉钉消息的封装
        :param market:
        :param quantity: 数量
        :param rate: 价格
        :return:
        '''
        try:
            res = BinanceAPI(api_key,api_secret).limit_future_order("SELL",market, quantity,"LONG", price)
            if res['orderId']:
                buy_info = "报警：币种为：{cointype}。做多卖单价为：{price}。卖单量为：{num}.".format(cointype=market,price=price,num=quantity)
                self.dingding_warn(buy_info)
                return res
        except BaseException as e:
            error_info = "报警：币种为：{cointype},做多多单失败.api返回内容为:{reject}".format(cointype=market,reject=res['msg'])
            self.dingding_warn(error_info+str(res))
            return res

    def open_buy_market_msg(self, market, quantity):
        '''
        合约开多 市价单
        :param market:
        :param quantity: 数量
        :param price: 价格
        :return:
        '''
        try:
            res = BinanceAPI(api_key, api_secret).market_future_order("BUY", market, quantity, "LONG")
            if res['orderId']:
                buy_info = "报警：币种为：{cointype}。开多买单量为：{num}".format(cointype=market,num=quantity)
                self.dingding_warn(buy_info)
                return res
        except BaseException as e:
            error_info = "报警：币种为：{cointype},开多多单失败.api返回内容为:{reject}".format(cointype=market, reject=res['msg'])

    def do_buy_market_msg(self, market, quantity,profit_usdt=0):
        '''
        合约平多 市价单
        :param market:
        :param quantity: 数量
        :param price: 价格
        :return:
        '''
        try:
            res = BinanceAPI(api_key, api_secret).market_future_order("SELL", market, quantity, "LONG")
            if res['orderId']:
                buy_info = "报警：币种为：{cointype}。做多卖单量为：{num}.".format(cointype=market,num=quantity)
                self.dingding_warn(buy_info)
                return res
        except BaseException as e:
            error_info = "报警：币种为：{cointype},开多多单失败.api返回内容为:{reject}".format(cointype=market, reject=res['msg'])

    def open_sell_market_msg(self, market, quantity):
        '''
        合约开空 市价单
        :param market:
        :param quantity: 数量
        :param price: 价格
        :return:
        '''
        try:
            res = BinanceAPI(api_key, api_secret).market_future_order("SELL", market, quantity, "SHORT")
            if res['orderId']:
                buy_info = "报警：币种为：{cointype}。网格开空买单量为：{num}".format(cointype=market,num=quantity)
                self.dingding_warn(buy_info)
                return res
        except BaseException as e:
            error_info = "报警：币种为：{cointype},开多多单失败.api返回内容为:{reject}".format(cointype=market, reject=res['msg'])

    def do_sell_market_msg(self, market, quantity,profit_usdt=0):
        '''
        合约平空 市价单
        :param market:
        :param quantity: 数量
        :param price: 价格
        :return:
        '''
        try:
            res = BinanceAPI(api_key, api_secret).market_future_order("BUY", market, quantity, "SHORT")

            if res['orderId']:

                buy_info = "报警：币种为：{cointype}。网格做空卖单量为：{num}.预计盈利{profit_num}".format(cointype=market,num=quantity,profit_num=profit_usdt)

                self.dingding_warn(buy_info)
                return res
        except BaseException as e:
            error_info = "报警：币种为：{cointype},开多多单失败.api返回内容为:{reject}".format(cointype=market, reject=res['msg'])


    # def open_buy_limit_msg(self,market, quantity, price):
    #     '''
    #     合约开多
    #     :param market:
    #     :param quantity: 数量
    #     :param price: 价格
    #     :return:
    #     '''
    #     try:
    #         res = BinanceAPI(api_key,api_secret).limit_future_order("BUY",market, quantity,"LONG", price)
    #         if res['orderId']:
    #             buy_info = "报警：币种为：{cointype}。开多买单价为：{price}。买单量为：{num}".format(cointype=market,price=price,num=quantity)
    #             self.dingding_warn(buy_info)
    #             return res
    #     except BaseException as e:
    #         error_info = "报警：币种为：{cointype},开多多单失败.api返回内容为:{reject}".format(cointype=market,reject=res['msg'])
    #         self.dingding_warn(error_info)



    # def open_sell_future_msg(self,market, quantity, price):
    #     '''
    #     合约开空单，带有钉钉消息
    #     :param market: 交易对
    #     :param quantity: 数量
    #     :param price: 价格
    #     :return:
    #     '''
    #     try:
    #         res = BinanceAPI(api_key,api_secret).limit_future_order('SELL', market, quantity,"SHORT", price)
    #         if res['orderId']:
    #             buy_info = "报警：币种为：{cointype}。开空买入价格为：{price}。数量为：{num}".format(cointype=market,price=price,num=quantity)
    #             self.dingding_warn(buy_info)
    #             return res
    #     except BaseException as e:
    #         error_info = "报警：币种为：{cointype},开空空单失败.api返回内容为:{reject}".format(cointype=market,reject=res['msg'])
    #         self.dingding_warn(error_info+str(res))
    #         return res
        
    def do_sell_future_msg(self,market, quantity, price,profit_usdt=0):
        '''
        合约做空单，带有钉钉消息
        :param market: 交易对
        :param quantity: 数量
        :param price: 价格
        :return:
        '''
        try:
            res = BinanceAPI(api_key,api_secret).limit_future_order('BUY', market, quantity,"SHORT", price)
            if res['orderId']:
                buy_info = "报警：币种为：{cointype}。做空卖单价为：{price}。数量为：{num}。".format(cointype=market,price=price,num=quantity)
                self.dingding_warn(buy_info)
                return res
        except BaseException as e:
            error_info = "报警：币种为：{cointype},做空空单失败.api返回内容为:{reject}".format(cointype=market,reject=res['msg'])
            self.dingding_warn(error_info+str(res))
            return res


    def buy_market_msg(self, market, quantity):
        '''
            现货市价买入
        :param market:
        :param quantity:
        :return:
        '''
        try:
            res = BinanceAPI(api_key,api_secret).buy_market(market, quantity)
            if res['orderId']:
                buy_info = "报警：币种为：{cointype}。买单量为：{num}".format(cointype=market,num=quantity)
                self.dingding_warn(buy_info)
                return res
        except BaseException as e:
            error_info = "报警：币种为：{cointype},买单失败.".format(cointype=market)
            self.dingding_warn(error_info)


    def sell_market_msg(self,market, quantity):
        '''
            现货市价卖出
        :param market:
        :param quantity: 数量
        :param rate: 价格
        :return:
        '''
        try:
            res = BinanceAPI(api_key,api_secret).sell_market(market, quantity)
            if res['orderId']:
                buy_info = "报警：币种为：{cointype}。卖单量为：{num}".format(cointype=market,num=quantity)
                self.dingding_warn(buy_info)
                return res
        except BaseException as e:
            error_info = "报警：币种为：{cointype},卖单失败".format(cointype=market)
            self.dingding_warn(error_info)
            return res

    def dingding_warn(self,text):
        headers = {'Content-Type': 'application/json;charset=utf-8'}
        api_url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % dingding_token
        json_text = self._msg(text)
        requests.post(api_url, json.dumps(json_text), headers=headers).content

    def _msg(self,text):
        json_text = {
            "msgtype": "text",
            "at": {
                "atMobiles": [
                    "11111"
                ],
                "isAtAll": False
            },
            "text": {
                "content": text
            }
        }
        return json_text

if __name__ == "__main__":
    msg = Message()
    print(msg.buy_limit_future_msg("EOSUSDT",3,2))