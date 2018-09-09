# -*- coding: utf-8 -*-
import sys
from account import OkexAccount
from account import FcoinAccount
import configparser
from strategy import Macd
import time

macd = Macd.Macd()

def strategy(account, klines, strategy, simulate):
    if strategy == "macd":
        cmd, kline = macd.getCmd(klines)
        print(cmd)
        kline.print_kline()
        if simulate:
            if cmd == "buy":
                account.simulateBuy(klines[0])
            elif cmd == "sell":
                account.simulateSell(klines[0])
        else:
            if cmd == "buy":
                account.buy(1)
            elif cmd == "sell":
                account.sell(1)


def simulateMarket(account):
    klines = account.getSimulateKlines()

    while len(klines) > 200:
        sublines = klines[0:200]
        strategy(account, sublines, "macd", True)
        klines.pop(0)

def realMarket(account):
    while True:
        klines, hasNew = account.getKlines()
        print(hasNew)
        if hasNew is True:
            strategy(account, klines, "macd", False)
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


