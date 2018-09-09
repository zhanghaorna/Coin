# -*- coding: utf-8 -*-

#简单queue结构，支持peek方法 put默认插入队头 get默认从队尾取，peek默认拿最新队一个元素

class Queue(object):

    def __init__(self):
        self.items = []

    def put(self, value):
        self.items.insert(0 , value)

    def get(self):
        if len(self.items) <= 0:
            raise Exception("Queue is empty")
        else:
            return self.items.pop()

    def size(self):
        return len(self.items)

    def peek(self):
        if len(self.items) <= 0:
            raise Exception("Queue is empty")
        else:
            return self.items[0]

    def values(self):
        return self.items

    def clear(self):
        self.items = []