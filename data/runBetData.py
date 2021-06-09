import os,json
from app.BinanceAPI import BinanceAPI
from app.authorization import api_key,api_secret

# linux
data_path = os.getcwd()+"/data/data.json"
# 本地调试
# data_path = os.getcwd()+""+"/data/data.json"
# windows
# data_path = os.getcwd() + "\data\data.json"
binan = BinanceAPI(api_key,api_secret)
class RunBetData:

    def _get_json_data(self):
        '''读取json文件'''
        tmp_json = {}
        with open(data_path, 'r') as f:
            tmp_json = json.load(f)
            f.close()
        return tmp_json


    def _modify_json_data(self,data):
        '''修改json文件'''
        with open(data_path, "w") as f:
            f.write(json.dumps(data, indent=4))
        f.close()


    ####------下面为输出函数--------####
    def get_coinList(self):
        data_json = self._get_json_data()
        return data_json["coinList"]

    def get_record_price(self,symbol):
        '''卖出后，step减一后，再读取上次买入的价格'''
        data_json = self._get_json_data()
        cur_step = self.get_future_step(symbol) - 1
        return data_json[symbol]['runBet']['recorded_price'][cur_step]

    def get_future_buy_price(self,symbol):
        data_json = self._get_json_data()
        return data_json[symbol]["runBet"]["future_buy_price"]


    def get_future_sell_price(self,symbol):
        data_json = self._get_json_data()
        return data_json[symbol]["runBet"]["future_sell_price"]

    def get_cointype(self,symbol):
        data_json = self._get_json_data()
        return data_json[symbol]["config"]["cointype"]


    def get_future_list(self,symbol):
        '''获取仓位数组'''
        data_json = self._get_json_data()
        return data_json[symbol]["config"]["future_quantity"]

    def get_future_quantity(self,symbol,exchange_method=True):
        '''
        :param exchange: True 代表买入，取买入的仓位 False：代表卖出，取卖出应该的仓位
        :return:
        '''

        data_json = self._get_json_data()
        future_step = data_json[symbol]["runBet"]["future_step"]
        cur_step = future_step if exchange_method else future_step - 1 # 买入与卖出操作对应的仓位不同
        quantity_arr = data_json[symbol]["config"]["future_quantity"]

        quantity = None
        if cur_step < len(quantity_arr): # 当前仓位 > 设置的仓位 取最后一位
            quantity = quantity_arr[0] if cur_step == 0 else quantity_arr[cur_step]
        else:
            quantity = quantity_arr[-1]
        return quantity

    def get_position_price(self,symbol):
        '''获取现货持仓均价'''
        data_json = self._get_json_data()
        return data_json[symbol]['runBet']['position_spot_price']
        
    def get_position(self,symbol):
        '''获取是否持仓均价平仓开关'''
        data_json = self._get_json_data()
        return data_json[symbol]['config']['position']

    def get_position_size(self,symbol):
        '''获取否持仓均价仓位数,满足则直接均价平'''
        data_json = self._get_json_data()
        return data_json[symbol]['config']['position_size']


    def get_future_step(self,symbol):
        '''获取期货仓位数'''
        data_json = self._get_json_data()
        return data_json[symbol]['runBet']['future_step']
     
    def get_profit_ratio(self,symbol):
        '''获取补仓比率'''
        data_json = self._get_json_data()
        return data_json[symbol]['config']['profit_ratio']
    
    def get_double_throw_ratio(self,symbol):
        '''获取止盈比率'''
        data_json = self._get_json_data()
        return data_json[symbol]['config']['double_throw_ratio']



    def modify_future_price(self, symbol,deal_price,step):
        data_json = self._get_json_data()
        right_size = len(str(deal_price).split(".")[1]) + 2
        data_json[symbol]["runBet"]["future_buy_price"] = round(deal_price * (1 + data_json[symbol]["config"]["profit_ratio"] / 100), right_size) # 保留2位小数
        data_json[symbol]["runBet"]["future_sell_price"] = round(deal_price * (1 - data_json[symbol]["config"]["double_throw_ratio"] / 100), right_size)
        data_json[symbol]["runBet"]["future_step"] = step
        self._modify_json_data(data_json)

    # def set_future_step(self,symbol,future_step,index=None):
    #     '''修改期货仓位数'''
    #     data_json = self._get_json_data()
    #     data_json[symbol]['runBet']['future_step'] = future_step
    #     if index != None:
    #         data_json[symbol]['config']['profit_ratio'] = index
    #         data_json[symbol]['config']['double_throw_ratio'] = index
    #
    #     self._modify_json_data(data_json)

    def add_record_price(self,symbol,value):
        '''记录交易价格'''
        data_json = self._get_json_data()
        data_json[symbol]['runBet']['recorded_price'].append(value)
        self._modify_json_data(data_json)


    def remove_record_price(self,symbol):
        '''记录交易价格'''
        data_json = self._get_json_data()
        del data_json[symbol]['runBet']['recorded_price'][-1]
        self._modify_json_data(data_json)

    def set_ratio(self,symbol):
        '''修改补仓止盈比率'''
        data_json = self._get_json_data()
        ratio_24hr = binan.get_ticker_24hour(symbol) #
        index = abs(ratio_24hr)

        if abs(ratio_24hr) >  10 : # 这是单边走势情况 只改变一方的比率
            if ratio_24hr > 0 : # 单边上涨，补仓比率不变
                data_json[symbol]['config']['profit_ratio'] = 6 + self.get_future_step(symbol) #
                data_json[symbol]['config']['double_throw_ratio'] = 5 - self.get_future_step(symbol)/4 #
            else: # 单边下跌
                data_json[symbol]['config']['double_throw_ratio'] =  6 + self.get_future_step(symbol)
                data_json[symbol]['config']['profit_ratio'] =  5 - self.get_future_step(symbol)/4

        else: # 系数内震荡行情

            data_json[symbol]['config']['double_throw_ratio'] = 2 +self.get_future_step(symbol)/4
            data_json[symbol]['config']['profit_ratio'] = 2 + self.get_future_step(symbol)/4
        self._modify_json_data(data_json)

    def delete_extra_zero(self, n):
        '''删除小数点后多余的0'''
        if isinstance(n, int):
            return n
        if isinstance(n, float):
            n = str(n).rstrip('0')  # 删除小数点后多余的0
            n = int(n.rstrip('.')) if n.endswith('.') else float(n)  # 只剩小数点直接转int，否则转回float
            return n

if __name__ == "__main__":
    instance = RunBetData()
    # print(instance.modify_price(8.87,instance.get_step()-1))
    print(instance.get_future_quantity())
