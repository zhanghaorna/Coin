# -*- coding: utf-8 -*-
import time
import logging

class Log(object):

    logger = None

    def __init__(self):
        pass

    @classmethod
    def getInstance(self):
        if self.logger == None:
            self.logger = logging.getLogger('')

            #文件日志
            file_handler = logging.FileHandler('{0}.log'.format(time.strftime('%Y-%m-%d', time.localtime(int(time.time())))))
            file_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))

            self.logger.addHandler(file_handler)
            self.logger.setLevel(logging.INFO)

        return self

    @classmethod
    def log(self, msg):
        self.logger.info(msg)
