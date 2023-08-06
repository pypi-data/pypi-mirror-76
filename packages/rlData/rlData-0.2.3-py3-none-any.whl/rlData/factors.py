
#coding:utf-8
'''
# File Name: factors.py
# Author: joyle
# mail: joyle.zhang@qq.com
# Created Time: 2020年08月03日 星期一 00时00分00秒
'''
from .utils import *

basic = FactorApiGenerator("basic")

class Factor:
    class Vip:
        def __init__(self):
            self.standard = FactorApiGenerator("factor/vip/standard")
            self.factor = FactorApiGenerator("factor/vip")

        def __getattr__(self, name):
            return self.factor.__getattr__(name)

    def __init__(self):
        self.standard = FactorApiGenerator("factor/standard")
        self.factor = FactorApiGenerator("factor")
        self.vip = Factor.Vip()

    def __getattr__(self, name):
        return self.factor.__getattr__(name)

factor = Factor()
