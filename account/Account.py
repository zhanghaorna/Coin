from utils import Queue

class Account(object):

    account = dict()
    fax = 0

    kline = Queue.Queue()
    MIN_DATA_COUNT = 26 * 3 + 1
    MAX_DATE = None

    def __init__(self):
        print()

    #获取K线数据
    def getKlines(self):
        raise NotImplementedError()

    #获取账户余额
    def getAccountBalance(self):
        raise NotImplementedError()

    #买币
    def buy(self, ratio, kline):
        raise NotImplementedError()

    def sell(self, ratio, kline):
        raise NotImplementedError()

    def initWithKeySecret(self, key, secret):
        raise NotImplementedError()