# -*- coding: utf-8 -*-
import utils.GlobalModel as gl

class KlineUtil(object):

    def __init__(self):
        pass

    #找klines [start,end] 的 macd 趋势
    @classmethod
    def findKlinesTrends(self, klines , start, end):
        assert isinstance(klines, list)

        trends = []

        if start >= end or len(klines) <= end:
            print('{0} {1} {2}'.format(start, end, len(klines)))
            return trends

        for i in range(start, end):
            if klines[i + 1].macd is None:
                break

            trend = gl.gl_macd_balance
            if klines[i].macd < klines[i + 1].macd:
                trend = gl.gl_macd_rise
            elif klines[i].macd > klines[i + 1].macd:
                trend = gl.gl_macd_drop

            if len(trends) == 0 or trends[-1] != trend:
                trends.append(trend)
        return trends

    #找klines的金叉 死叉点位
    @classmethod
    def findCross(self, klines, count):
        assert isinstance(klines, list)

        index = []
        crosses = []

        for i in range(0, len(klines) - 1):
            if klines[i].cha is not None:
                index.append(i)
                crosses.append(klines[i])
                if len(crosses) >= count:
                    return index, crosses
        return index, crosses

    @classmethod
    def findRangeBelowValue(self, klines, start, end, value):
        assert isinstance(klines, list)

        if start > end or len(klines) <= end:
            return False

        for i in range(start, end + 1):
            if klines[i].dif >= value:
                return False

        return True

    @classmethod
    def findRangeAboveValue(self, klines, start, end, value):
        assert isinstance(klines, list)

        if start > end or len(klines) <= end:
            return False

        for i in range(start, end + 1):
            if klines[i].dif <= value:
                return False

        return True