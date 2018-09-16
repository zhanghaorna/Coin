# -*- coding: utf-8 -*-
import sys
from account import OkexAccount
from account import FcoinAccount
import configparser
from strategy import Macd
import time
from log import Log

macd = Macd.Macd()

def strategy(account, klines, strategy, simulate):
    if strategy == "macd":
        operate, kline = macd.getCmd(klines)
        print(operate.cmd)
        kline.print_kline()
        if simulate:
            if operate.cmd == "buy":
                account.simulateBuy(kline, operate)
            elif operate.cmd == "sell":
                account.simulateSell(kline)
        else:
            if operate.cmd == "buy":
                account.buy(1)
            elif operate.cmd == "sell":
                account.sell(1)


def simulateMarket(account):
    klines = account.getSimulateKlines()
    # klines = macd.getMacdInfo(klines)
    # for kline in klines:
    #     Log.Log.getInstance().logKline(kline)
    # klines.reverse()

    while len(klines) > 200:
        sublines = klines[0:200]
        strategy(account, sublines, "macd", True)
        klines.pop(0)

def realMarket(account):
    while True:
        try:
            klines, hasNew = account.getKlines()
            print(hasNew)
            if hasNew is True:
                strategy(account, klines, "macd", False)
        except Exception as ex:
            Log.Log.getInstance().log('run error {0}'.format(ex))
        finally:
            time.sleep(30)

def run(market, apiKey, secret):
    if market == "okex":
        account = OkexAccount.OkexAccount()
    elif market == "fcoin":
        account = FcoinAccount.FcoinAccount()
    else:
        raise RuntimeError('not support market', market)

    account.initWithKeySecret(apiKey, secret)

    cf = configparser.ConfigParser()
    cf.read('config.ini')
    account.ruler(cf)
    simulate = cf.get('strategy', 'simulate')


    #如果模拟盘
    if simulate == '1':
        fax = cf.get('simulation', 'fax')
        coinType = cf.get('simulation', 'coin')
        coinCount = cf.get('simulation', 'count')
        account.fax = float(fax)
        account.account[coinType] = coinCount
        simulateMarket(account)
    #实盘
    else:
        realMarket(account)

def main(argv):
    cf = configparser.ConfigParser()
    cf.read('config.ini')
    key = cf.get('secret', 'key')
    secret = cf.get('secret', 'secret')
    market = cf.get('secret', 'market')

    if key is None or secret is None or market is None:
        print('you must specify secret in config.ini')
        sys.exit()


    print('交易所:', market)
    print('apiKey:', key)
    print('secretKey:', secret)
    run(market, key, secret)

if __name__ == "__main__":
    main(sys.argv[1:])


