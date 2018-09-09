# -*- coding: utf-8 -*-
import talib
import numpy as np
import math as math
from market import Kline
from strategy import Kdj
from operator import attrgetter

kdj = Kdj.Kdj()

class Macd(object):

    next_cmd = "see"

    def __init__(self):
        print()

    def getMacdInfo(self, klines):
        if len(klines) == 0:
            raise RuntimeError('Macd分析必须有足够的数据')

        assert isinstance(klines, list)

        klines = sorted(klines, key=attrgetter('_date'))

        prices = []
        for kline in klines:
             prices.append(kline._close)

        difs, deas, macds = talib.MACD(np.array(prices).astype('double'))

        for (dif, dea, macd, kline) in zip(np.nditer(difs), np.nditer(deas), np.nditer(macds), klines):
            kline.dif = dif
            kline.dea = dea
            kline.macd = macd

        kdj.getKdjInfo(klines)

        klines.reverse()

        for i in range(0, len(klines) - 1):
            if klines[i].macd > 0 and klines[i+1].macd < 0:
                klines[i].cha = 0
            elif klines[i].macd < 0 and klines[i+1].macd > 0:
                klines[i].cha = 1
        return klines

    def findCha(self, klines, count):
        assert isinstance(klines, list)

        chalist = []

        for i in range(0, len(klines) - 1):
            if klines[i].cha != None:
                chalist.append(klines[i])
                if len(chalist) >= count:
                    return chalist
        return chalist




    def needBuy(self, new, olds):
        assert isinstance(new, Kline.Kline)
        assert isinstance(olds, list)


        #
        # #rule1 MACD零轴附近金叉 (30min 小于 8)
        # if new.macd > 0 and olds[0].macd < 0 and math.fabs(float(new.dif)) < 8:
        #     return "buy"

        #rule2 MACD低位金叉的买点(先观望，往前在找一个金叉，如果小于自己，则买入)
        if new.macd > 0 and olds[0].macd < 0 and new.dif < 0:
            lastTwoCha = self.findCha(olds, 2)
            if lastTwoCha[1].dif < new.dif:
                return "buy"

        #rule3 MACD零轴上方形成二次金叉
        if new.macd > 0 and olds[0].macd < 0 and new.dif > 0:
            lastTwoCha = self.findCha(olds, 2)
            if len(lastTwoCha) == 2:
                if lastTwoCha[0].dif < new.dif:
                    return "buy"


        return "see"

    def needSell(self, new, olds):
        assert isinstance(new, Kline.Kline)
        assert isinstance(olds, list)


        #rule2 MACD 零轴下方死叉
        if new.macd <= 0 and olds[0].macd > 0:
            return "sell"

        return "see"
        

    #DIF线 上穿DEA线(分0线下方和0线上方)
    def isJingCha(self, new, olds):
        assert isinstance(new, Kline.Kline)
        assert isinstance(olds, list)

        # dif刚开始上穿金叉线
        if  new.macd > 0 and olds[0].macd < 0 :
            return "buy"
        else:
            return "see"

    # DIF线 下穿DEA线(分0线下方和0线上方)
    def isSiCha(self, new, olds):
        assert isinstance(new, Kline.Kline)
        assert isinstance(olds, list)

        # dif刚开始下穿金叉线
        if new.macd < 0 and olds[0].macd > 0:
            return "sell"
        else:
            return "see"



    def getCmd(self, klines):
        klines = self.getMacdInfo(klines)

        last = klines[1]
        olds = klines[2:]

        cmd = self.needBuy(last, olds)
        if cmd == "see":
            cmd = self.needSell(last, olds)

        if cmd != "see" and self.next_cmd == "see":
            self.next_cmd = cmd

        if self.next_cmd == "buy":
            if last.k < 20:
                cmd = "buy"
            else:
                cmd = "see"
        if self.next_cmd == "sell":
            print('sell')
            last.print_kline()
            if last.k > 80 or last.d > 80:
                cmd = "sell"
            else:
                cmd = "see"

        if cmd != "see":
            self.next_cmd = "see"

        return cmd, last
