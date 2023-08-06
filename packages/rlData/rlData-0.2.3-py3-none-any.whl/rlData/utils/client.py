#coding:utf-8
'''
# File Name: client.py
# Author: joyle
# mail: joyle.zhang@qq.com
# Created Time: 2020年08月03日 星期一 00时00分00秒
'''
import os
import http.client
import urllib
import json
from passlib.context import CryptContext

__all__ = [
    "client",
    "login",
]

DEFAULT_HOST = os.getenv("RLDATA_HOST","121.37.138.1")
DEFAULT_PORT = os.getenv("RLDATA_PORT",8000)
DEFAULT_VERSION = os.getenv("RLDATA_VERSION","v1")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Client(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__( self, *, host=DEFAULT_HOST, port=DEFAULT_PORT, apiVersion=DEFAULT_VERSION):
        self.host=host
        self.port=port
        self.baseUrl=f"/{apiVersion}"
        self.token=None

    def __call__( self, *, host=DEFAULT_HOST, port=DEFAULT_PORT, apiVersion=DEFAULT_VERSION):
        self.host=host
        self.port=port
        self.baseUrl=f"/{apiVersion}"
        self.token=None

    class ClientConn:
        def __init__(self,host,port):
            self.host=host
            self.port=port

        def __enter__(self):
            self.conn = http.client.HTTPConnection( self.host, self.port )
            return self.conn

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.conn.close()

    def request( self, method, url, body=None, headers={"accept": "application/json"}, *, encode_chunked=False ):
        retobj = None
        if self.token:
            headers.update({"Authorization": f"{self.token['token_type']} {self.token['access_token']}"})

        with self.ClientConn(self.host,self.port) as conn:
            conn.request(method, f"{self.baseUrl}{url}", body, headers, encode_chunked=encode_chunked)
            res = conn.getresponse()

            rets = res.read()

            if rets:
                retobj = json.loads(rets)

            if self.token and "access_token" in retobj.keys():
                self.token["access_token"] = retobj["access_token"]
                del retobj["access_token"]

            return res.status, retobj

    def login(self, username, password ):
        """ 
        
        """
        
        params = urllib.parse.urlencode(dict({'username': username, 'password': pwd_context.hash(password)}))
        header = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        with self.ClientConn(self.host,self.port) as conn:
            conn.request("POST", "/token", body=params, headers=header)
            res = conn.getresponse()
            retobj = json.loads(res.read())
            if res.status==200:
                self.token=retobj

            return res.status, retobj

client=Client()

def login(username,password):
    return client.login(username,password)

if __name__ == '__main__':
    a = Client()
    s, ret = a.request("GET", "/factor/daily_price?stocks=300012,600519")
    print(ret)
    s, ret = a.login("joyle","j0y138oe")
    print(ret)
    s, ret = a.request("GET", "/factor/daily_price?stocks=300012,600519")
    print(ret)
