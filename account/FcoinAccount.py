from account import Account
from market import Kline
from log import Log
import fcoin

class FcoinAccount(Account.Account):

    def __init__(self):
        print('init FcoinAccount')
        self.api = None
        self.symbol = None
        self.resolution = None
        self.base = None
        self.quote = None

    def initWithKeySecret(self, key, secret):
        self.api = fcoin.authorize(key, secret)

    #规则化 将通用参数转为交易所实际参数
    def ruler(self, cf):
        self.base = cf.get('strategy', 'base')
        self.quote = cf.get('strategy', 'quote')
        self.symbol = self.base  + self.quote
        type = cf.get('strategy', 'type')
        if type == '1min':
            self.resolution = "M1"
        elif type == '3min':
            self.resolution = "M3"
        elif type == '5min':
            self.resolution = "M5"
        elif type == '15min':
            self.resolution = "M15"
        elif type == '30min':
            self.resolution = "M30"
        elif type == '1hour':
            self.resolution = "H1"
        elif type == '4hour':
            self.resolution = "H4"
        elif type == '6hour':
            self.resolution = "H6"
        elif type == '1day':
            self.resolution = "D1"
        elif type == '1week':
            self.resolution = "W1"
        elif type == '1month':
            self.resolution = "MN"


    def getKlines(self):
        if self.symbol is None or self.resolution is None:
            raise RuntimeError('fcoin 必须指定交易对和')

        # 没有历史K线数据，需要发HTTP请求拉回来，MACD至少需要26。拉3倍的数据
        params = dict()
        params['limit'] = max(self.MIN_DATA_COUNT - self.kline.size(), 1)

        result = self.api.signed_request('GET', 'https://api.fcoin.com/v2/market/candles/{0}/{1}'.format(self.resolution, self.symbol), params=params)

        maxDate = None

        for kline in result['data']:
            date = kline['id'] * 1000
            if maxDate is None or maxDate < date:
                maxDate = date
            k = Kline.Kline(date, kline['open'], kline['high'], kline['low'], kline['close'], kline['base_vol'])
            self.kline.put(k)

        hasNew = False
        if self.MAX_DATE is None or self.MAX_DATE < maxDate:
            self.MAX_DATE = maxDate
            hasNew = True

        return self.kline.values(), hasNew

    def getAccountBalance(self):
        balance = self.api.get_balance()
        coins = balance['data']
        for coin in coins:
            self.account[coin['currency']] = coin['available']
        return self.account

    def buy(self, ratio, kline):
        account = self.getAccountBalance()
        if float(account.get(self.quote, 0)) < 5 and False:
            pass
        else:
            ticker = self.api.get_ticker(self.symbol)
            ticker = ticker['data']
            tickerSymbol = ticker['type']
            if tickerSymbol != ("ticker." + self.symbol):
                raise RuntimeError('error symbol' + tickerSymbol)

            sellOne = ticker['ticker'][4]
            #挂单卖一价(先看看收益,之后在看看要不要改为买一)
            Log.Log.getInstance().log('buy order {0} in price {1} ratio {2}'.format(self.base, sellOne, ratio))
            Log.Log.getInstance().log(kline.print_kline())

    def sell(self, ratio, kline):
        account = self.getAccountBalance()
        if float(account.get(self.base, 0)) < 0.0001 and False:
            pass
        else:
            ticker = self.api.get_ticker(self.symbol)
            ticker = ticker['data']
            tickerSymbol = ticker['type']
            if tickerSymbol != ("ticker." + self.symbol):
                raise RuntimeError('error symbol' + tickerSymbol)

            buyOne = ticker['ticker'][2]
            #挂单买一价(立即卖出)
            Log.Log.getInstance().log('sell order {0} in price {1} ratio {2}'.format(self.base, buyOne, ratio))
            Log.Log.getInstance().log(kline.print_kline())