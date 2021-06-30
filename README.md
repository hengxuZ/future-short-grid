> 如果你还未使用过该项目，请通过[该链接](https://github.com/hengxuZ/binance-quantization)，查看第一版本。有助于你更好的了解本项目。 

### 🎉第四版本🎉 （合约趋势做空网格）
---

### 介绍
传统网格都是做震荡和上涨的行情，那么当行情处于大跌或者看跌中，您可以使用该项目来震荡+下跌的行情。

须知：您需要对当前行情表达自己的看法。择行情使用符合的策略，做到稳赚网格🤖️
如果您对后面的走势看空，完全可以选择这款产品
如果你看多，那么也可以使用v2 👇
> v2震荡上升网格：[访问地址](https://github.com/hengxuZ/spot-trend-grid)


### 项目特点：🎉
1. 简单易上手
2. 安全(不用将api_secret告诉他人)
3.趋势判断，不在固定点位开单，选择更优的开仓点位
4.单项目支持多币对

### 如何启动

1. 修改app目录下的authorization文件

```
api_key='你的key'
api_secret='你的secret'

dingding_token = '申请钉钉群助手的token'   # （若不会申请，请加我个人微信）
```

如果你还没有币安账号： [注册页面](https://www.binancezh.io/zh-CN/register?ref=OW7U53AB)  [免翻墙地址](https://www.binancezh.cc/zh-CN/register?ref=OW7U53AB)
交易返佣20%  注册立刻返现5元，充值交易再返现15元（下方加微信返现）。

或者可以注册火币账号：[注册页面](https://www.huobi.ms/zh-cn/topic/double-reward/?invite_code=w2732223)交易返佣15% 注册立刻返现5元，充值并且交易再返现10元

>交易返佣计算公式：交易金额1W元 * 手续费比率0.1% * 0.02 = 2元（交易1w节约2元）

申请api_key地址: [币安API管理页面](https://www.binance.com/cn/usercenter/settings/api-management)
>申请api_key时一定要勾选上 
1.允许现货及杠杆交易 
2.允许合约 

2. 安装依赖包
'''
pip install requests
'''

3. 修改data/data.json配置文件  （参数详细解读->[一定要看](https://github.com/hengxuZ/binance-quantization/blob/master/dev-ReadMe.md)）

```
由于本版本支持多币对，配置文件略有不同
1.coinList中填入你要执行的币对，下方的该币对一一对应配置项
{
    "coinList": [EOSUSDT","ONTUSDT"],
    "EOSUSDT": {
        "runBet": {
            "future_buy_price": 6.206,
            "future_sell_price": 5.529,
            "future_step": 1,
            "recorded_price": []                          # 用于记录每次卖出(空单的开仓对应的是卖出，你可以理解为买入)的价格
        },
        "config": {
            "profit_ratio": 5.5,
            "double_throw_ratio": 6.0,
            "future_quantity": [
                20
            ]
        }
    },
    "ONTUSDT": {
        "runBet": {
            "future_buy_price": 1,
            "future_sell_price": 0.9,
            "future_step": 0,
            "recorded_price": []                          # 用于记录每次卖出(空单的开仓对应的是卖出，你可以理解为买入)的价格
        },
        "config": {
            "profit_ratio": 5.25,
            "double_throw_ratio": 5.5,
            "future_quantity": [
                100
            ]
        }
    },
```

4. 运行主文件
```
# nohup python3 run.py > run.log &  #后台挂载 程序买卖、异常会通过钉钉通知(推荐使用钉钉模式启动👍)
```
---

如果您不想那么麻烦，又是python、linux 服务器。可以使用下面链接注册派网。体验网格交易
![派网注册](https://www.pionex.cc/zh-CN/sign/ref/gP7byIO9)（通过该链接注册的用户，加我立马返现2元）

### 注意事项（一定要看）
- 由于交易所的api在大陆无法访问，默认运行环境是国外的服务器,默认环境是python3(linux自带的是python2)

- 如果您使用的交易所为币安，那么请保证账户里有足够的bnb
    - 手续费足够低
    - 确保购买的币种完整(如果没有bnb,比如购买1个eth,其中你只会得到0.999。其中0.001作为手续费支付了)


- 第一版本现货账户保证有足够的U
   
- 由于补仓比率是动态的，目前默认最小为5%。如果您认为过大，建议您修改文件夹data下的RunbetData.py文件
```加粗的数值均可调整，适合你风险系数的比率
    def set_ratio(self,symbol):
        '''修改补仓止盈比率'''
        data_json = self._get_json_data()
        ratio_24hr = binan.get_ticker_24hour(symbol) #
        index = abs(ratio_24hr)

        if abs(ratio_24hr) >  **6** : # 今日24小时波动比率
            if ratio_24hr > 0 : # 单边上涨，补仓比率不变
                data_json['config']['profit_ratio'] =  **7** + self.get_step()/4  #
                data_json['config']['double_throw_ratio'] = **5**
            else: # 单边下跌
                data_json['config']['double_throw_ratio'] =  **7** + self.get_step()/4
                data_json['config']['profit_ratio'] =  **5**

        else: # 系数内震荡行情

            data_json['config']['double_throw_ratio'] = **5** + self.get_step() / 4
            data_json['config']['profit_ratio'] = **5** + self.get_step() / 4
        self._modify_json_data(data_json)
```

### 钉钉预警

如果您想使用钉钉通知，那么你需要创建一个钉钉群，然后加入自定义机器人。最后将机器人的token粘贴到authorization文件中的dingding_token
关键词输入：报警

#### 钉钉通知交易截图

![钉钉交易信息](https://s3.ax1x.com/2021/02/01/yZSi1x.jpg)
#### 25日实战收益
![收益图](https://z3.ax1x.com/2021/05/15/gyLTB9.jpg)


### 私人微信：欢迎志同道合的朋友一同探讨，一起进步。
![qq交流群](https://img02.sogoucdn.com/app/a/100520146/D179E91E279E65E3DD642C24D482D23D)
#### qq群号：1143200770

![币圈快讯爬取群](https://s3.ax1x.com/2021/02/01/yZSU4s.jpg)
![钉钉群二维码](https://i0.hdslb.com/bfs/album/4f50bfd7f1fddaa7c340bc06d7ce078404670fb2.jpg)

麻烦备注来自github
### 钉钉设置教程
![钉钉设置教程](https://s3.ax1x.com/2021/01/08/suMVIK.png)


### 免责申明
本项目不构成投资建议，投资者应独立决策并自行承担风险
币圈有风险，入圈须谨慎。

> 🚫风险提示：防范以“虚拟货币”“区块链”名义进行非法集资的风险。
