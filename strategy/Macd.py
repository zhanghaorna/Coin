# -*- coding: utf-8 -*-
import talib
import numpy as np
import math as math
from market import Kline
from strategy import Kdj
from operator import attrgetter
import utils.GlobalModel as gl
from utils import KlineUtil
from strategy import Operate

kdj = Kdj.Kdj()

class Macd(object):

    next_operate = Operate.Operate("see", "观望")

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

    def macdTech(self, new, olds):
        assert isinstance(new, Kline.Kline)
        assert isinstance(olds, list)

        #1 漫步青云(零轴之上死叉 然后下穿0轴，然后在上升0轴之上金叉)
        if new.macd > 0 and olds[0].macd < 0 and new.dif > 0:
            indexs, crosses = KlineUtil.KlineUtil.findCross(olds, 1)
            if len(crosses) == 1:
                lastCrossKline = crosses[0]
                if lastCrossKline.dif > 0:
                    for i in range(0, indexs[0] + 1):
                        if olds[i].dif < 0:
                            return Operate.Operate("buy", "漫步青云")

        #2 天鹏展翅(0轴以下金叉，但没有上穿0轴就回调了，但没有死叉就再次反转向上)
        if new.macd > olds[0].macd:
            indexs, crosses = KlineUtil.KlineUtil.findCross(olds, 1)
            if len(crosses) == 1:
                lastCrossKline = crosses[0]
                if lastCrossKline.isJinCha() and lastCrossKline.dif < 0:
                    trends = KlineUtil.KlineUtil.findKlinesTrends(olds, 0, indexs[0])
                    if len(trends) == 2 and trends[0] == gl.gl_macd_rise and trends[1] == gl.gl_macd_drop:
                        if KlineUtil.KlineUtil.findRangeBelowValue(olds, 0, indexs[0], 0):
                            return Operate.Operate("buy", "天棚展翅")

        #rule3 空中缆绳(先有一段升降趋势，然后DIF和DEA在零轴之上持续搅合一段时间，然后突然DIF突然分开，形成买点)
        #暂时将macd小于0.5认为两条线搅合在一起
        if new.macd > olds[0].macd and new.dif > 0 and new.macd > 0.5 and math.fabs(olds[0].macd) < 0.5:
            stirCount = 1

            for index in range(len(olds)):
                if math.fabs(olds[index].macd) < 0.5 and olds[index].dif > 0:
                    stirCount = stirCount + 1
                else:
                    if stirCount > 3:
                        trends = KlineUtil.KlineUtil.findKlinesTrends(olds, index, len(olds) - 1)
                        if len(trends) >= 2 and trends[0] == gl.gl_macd_rise and trends[1] == gl.gl_macd_drop:
                            return Operate.Operate("buy", "空中缆绳")
                    break

        #rule4  空中缆车(零轴之上死叉，但不下穿零轴，过几天再次在零轴之上金叉 看看需不需要考虑放量)
        if new.macd > 0 and olds[0].macd < 0 and new.dif > 0:
            indexs, crosses = KlineUtil.KlineUtil.findCross(olds, 1)
            if len(crosses) == 1:
                lastCrossKline = crosses[0]
                if lastCrossKline.dif > 0:
                    if KlineUtil.KlineUtil.findRangeAboveValue(olds, 0, indexs[0], 0):
                        trends = KlineUtil.KlineUtil.findKlinesTrends(olds, 0, indexs[0])
                        if len(trends) == 2 and trends[0] == gl.gl_macd_drop and trends[1] == gl.gl_macd_rise:
                            return Operate.Operate("buy", "空中缆车")

        #rule5 海底电缆(零轴一下金叉，然后DIF和DEA线粘合起来在零轴以下运行很长时间(暂时认为15分钟)，然后开始发散，形成买点)
        if new.macd > olds[0].macd and new.dif < 0:
            if KlineUtil.KlineUtil.findRangeBelowValue(olds, 0, min(15, len(olds) - 1), 0):
                stirCount = 0
                for i in range(0, min(20, len(olds))):
                    if math.fabs(olds[i].macd) < 0.5 and olds[i].dif < 0:
                        stirCount = stirCount + 1
                    else:
                        break
                if stirCount >= 15:
                    return Operate.Operate("buy", "海底电缆")

        #rule6 海底捞月(零轴以下二次金叉)
        if new.macd > 0 and olds[0].macd < 0 and new.dif < 0:
            indexes, crosses = KlineUtil.KlineUtil.findCross(olds, 2)
            if len(crosses) == 2:
                if KlineUtil.KlineUtil.findRangeBelowValue(olds, 0, indexes[1], 0):
                    return Operate.Operate("buy", "海底捞月")


        #rule7 死叉卖出?
        if new.macd < 0 and olds[0].macd > 0:
            return Operate.Operate("sell", "死叉")

        return Operate.Operate("see", "观望")

    def getCmd(self, klines):
        klines = self.getMacdInfo(klines)

        last = klines[1]
        olds = klines[2:]

        operate = self.macdTech(last, olds)

        if operate.cmd != "see":
            self.next_operate = operate

        if self.next_operate.cmd == "buy":
            if last.k < 18:
                operate = self.next_operate
            else:
                operate.cmd = "see"
                operate.description = "观望"
        if self.next_operate.cmd == "sell":
            if last.k > 82:
                operate = self.next_operate
            else:
                operate.cmd = "see"
                operate.description = "观望"

        if operate.cmd != "see":
            self.next_operate = Operate.Operate("see", "观望")

        return operate, last
