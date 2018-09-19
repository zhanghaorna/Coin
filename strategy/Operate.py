# -*- coding: utf-8 -*-

class Operate(object):

    def __init__(self, cmd, description):
        self.cmd = cmd
        self.description = description

    def clone(self):
        return Operate(self.cmd, self.description)