# -*- coding: utf-8 -*-
import talib
import numpy as np

class Kdj(object):
    def __init__(self):
        print()

    def getKdjInfo(self, klines):
        if len(klines) == 0:
            raise RuntimeError('kdj分析必须有足够的数据')

        assert isinstance(klines, list)

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

        return klines