# -*- coding: utf-8 -*-
import talib
import numpy as np
from strategy import Macd
from operator import attrgetter
from strategy import Operate


class Kdj(object):
    def __init__(self):
        print()

    @classmethod
    def getKdjInfo(self, klines):
        if len(klines) == 0:
            raise RuntimeError('kdj分析必须有足够的数据')

        assert isinstance(klines, list)

        klines = sorted(klines, key=attrgetter('_date'))

        close = []
        high = []
        low = []
        for kline in klines:
            close.append(kline._close)
            high.append(kline._high)
            low.append(kline._low)

        kv, dv = talib.STOCH(np.array(high).astype('double'), np.array(low).astype('double'), np.array(close).astype('double'))

        for (k, d, kline) in zip(np.nditer(kv), np.nditer(dv), klines):
            kline.k = k
            kline.d = d

        klines = sorted(klines, key=attrgetter('_date'), reverse=True)

        return klines

    def getCmd(self, klines):
        klines = self.getKdjInfo(klines)
        Macd.Macd.getMacdInfo(klines)

        last = klines[1]
        operate = Operate.Operate("see", "观望")
        if last.k < 10:
            operate = Operate.Operate("buy", "kdj买入")
        elif last.k > 80:
            operate = Operate.Operate("sell", "kdj卖出")

        print(last.k)

        return operate,klines[0]

