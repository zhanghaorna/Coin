from account import Account
from market import Kline
import requests
from log import Log

class OkexAccount(Account.Account):

    def __init__(self):
        print('init okexAccount')
        self.symbol = None
        self.type = None

    def initWithKeySecret(self, key, secret):
        pass

    def ruler(self, cf):
        base = cf.get('strategy','base')
        quote = cf.get('strategy','quote')
        self.symbol = base + '_' + quote
        self.type = cf.get('strategy', 'type')

    def getCountKlines(self, count):
        url = 'https://www.okex.com/api/v1/kline.do?symbol={0}&type={1}&size={2}'.format(self.symbol, self.type, count)
        r = requests.get(url, headers={'contentType': 'application/x-www-form-urlencoded'})

        klines = []
        for kline in r.json():
            klines.append(Kline.Kline(kline[0], kline[1], kline[2], kline[3], kline[4], kline[5]))

        return klines

    def getSimulateKlines(self):
        return self.getCountKlines(2000)

    def getKlines(self):
        if self.symbol is None or self.type is None:
            raise RuntimeError('okex 必须指定交易对和')

        maxDate = None

        count = max(self.MIN_DATA_COUNT - self.kline.size(), 1)
        klines = self.getCountKlines(count)
        for kline in klines:
            if maxDate is None or maxDate < kline._date:
                maxDate = kline._date

        hasNew = False
        if self.MAX_DATE is None or self.MAX_DATE < maxDate:
            self.MAX_DATE = maxDate
            hasNew = True
        return klines, hasNew

    def simulateBuy(self, kline, operate):
        Log.Log.getInstance().log('buy {0}'.format(kline.print_kline()))
        if float(self.account.get('usdt', 0)) < 10:
            pass
        else:
            count = float(self.account['usdt']) / float(kline._close)
            self.account['btc'] = float(count * (1 - self.fax))
            Log.Log.getInstance().log('buy {0} btc cost {1} usdt through {2}'.format(self.account['btc'], float(self.account['usdt']), operate.description))
            self.account['usdt'] = 0

    def simulateSell(self, kline):
        Log.Log.getInstance().log('sell {0}'.format(kline.print_kline()))
        if float(self.account.get('btc', 0)) < 0.0001:
            pass
        else:
            count = float(self.account['btc']) * float(kline._close)
            self.account['usdt'] = float(count * (1 - self.fax))
            Log.Log.getInstance().log('sell {0} btc get {1} usdt'.format(self.account['btc'], self.account['usdt']))
            self.account['btc'] = 0

            Log.Log.getInstance().log('profit {0} usdt'.format(float(self.account['usdt']) - 1000))


    def buy(self, kline):
        if float(self.account.get('usdt', 0)) < 10:
            print()
            #Log.Log.getInstance().log('not enough money')
        else:
            count = float(self.account['usdt']) / float(kline._close)
            self.account['btc'] = float(count * (1 - self.fax))
            Log.Log.getInstance().log('buy {0} btc cost {1} usdt'.format(count, float(self.account['usdt'])))
            self.account['usdt'] = 0

    def sell(self, kline):
        if float(self.account.get('btc', 0)) < 0.0001:
            print()
            #Log.Log.getInstance().log('not enough btc to sell')
        else:
            count = float(self.account['btc']) * float(kline._close)
            self.account['usdt'] = float(count * (1 - self.fax))
            Log.Log.getInstance().log('sell {0} btc get {1} usdt'.format(self.account['btc'], count))
            self.account['btc'] = 0

            Log.Log.getInstance().log('profit {0} usdt'.format(float(self.account['usdt']) - 1000))




