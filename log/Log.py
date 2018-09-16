# -*- coding: utf-8 -*-
import time
import logging
import configparser

class Log(object):

    logger = None
    klineLogger = None

    def __init__(self):
        pass

    @classmethod
    def getInstance(self):
        if self.logger == None:
            self.logger = logging.getLogger('')

            cf = configparser.ConfigParser()
            cf.read('config.ini')
            market = cf.get('secret', 'market')
            if market is None:
                market = ""

            #文件日志
            file_handler = logging.FileHandler('{0}_{1}.log'.format(time.strftime('%Y-%m-%d', time.localtime(int(time.time()))), market))
            file_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))

            self.logger.addHandler(file_handler)
            self.logger.setLevel(logging.INFO)

        if self.klineLogger == None:
            self.klineLogger = logging.getLogger('kline')

            #文件日志
            file_handler = logging.FileHandler('kline.log')
            file_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))

            self.klineLogger.addHandler(file_handler)
            self.klineLogger.setLevel(logging.INFO)


        return self

    @classmethod
    def logKline(self, kline):
        self.klineLogger.info(kline.print_kline())


    @classmethod
    def log(self, msg):
        self.logger.info(msg)


