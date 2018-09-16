# -*- coding: utf-8 -*-

import time

class Kline(object):

    dif = None
    dea = None
    macd = None

    k = None
    d = None

    #金叉为0 死叉为1
    cha = None

    def __init__(self, _date, _open, _high, _low, _close, _volume):
        self._date = _date
        self._open = _open
        self._high = _high
        self._low = _low
        self._close = _close
        self._volume = _volume

    def print_kline(self):
        str = 'date:{0} dif:{1} dea:{2} macd:{3} close:{4} k:{5} d:{6}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(self._date) / 1000)), self.dif, self.dea, self.macd, self._close, self.k, self.d)
        print(str)
        return str

    def isJinCha(self):
        return self.cha == 0

    def isSiCha(self):
        return self.cha == 1

    def simple_kline(self):
        str = 'date:{0} close:{1}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(self._date) / 1000)), self._close)
        return str
