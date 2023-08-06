#coding:utf-8
'''
# File Name: tools.py
# Author: joyle
# mail: joyle.zhang@qq.com
# Created Time: 2020年08月03日 星期一 00时00分00秒
'''
import pandas as pd
from .client import client

__all__=[
    "getList",
    "getFactor",
]

def getList(group):
    """
    
    """
    url = f"/{group}/"

    status, ret = client.request("GET", url=url)

    if status == 200:
        ret=pd.DataFrame(ret['data'])

    return status, ret

def getFactor(group, key, *, factors=None,isymbol=None,stocks=None,startdate=None,enddate=None,period=None):
    """
    
    """
    if isymbol is None and stocks is None:
        return 400, {'detail': 'isymbol和stocks参数至少需要设置一个'}

    params=""

    if factors:
        if isinstance(factors,list):
            factors = ','.join(factors)
        params = f"{params}&fields={factors}"
    if isymbol:
        params = f"{params}&isymbol={isymbol}"
    if stocks:
        if isinstance(stocks, list):
            stocks = ','.join(stocks)
        params = f"{params}&stocks={stocks}"
    if startdate:
        params = f"{params}&startdate={startdate}"
    if enddate:
        params = f"{params}&enddate={enddate}"
    if period:
        params = f"{params}&period={period}"

    params = params[1:]

    url = f"/{group}/{key}?{params}"

    status, ret = client.request("GET", url=url)

    if status == 200:
        ret=pd.DataFrame(ret['data'])

    return status, ret
