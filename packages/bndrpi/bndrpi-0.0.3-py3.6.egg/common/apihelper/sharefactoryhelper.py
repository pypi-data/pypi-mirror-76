#coding:utf-8

import sys
import json
import requests
import threading


class ShareFactoryHelper:
    def __init__(self, url):
        self.url = url

    def __Post(self, url='', data=''):

        r = requests.post(url,data)

        if not r:
            return None
        else:
            return r.text
        #return requests.post(url,data)

    def __Get(self, url=''):
        
        return requests.get(url)

    def TransWeightAsync(self,data):
        """
        异步同步称重数据，获取相关称重数据后调用，无需关系接收端是否保存成功
        参数：
            data：同步的数据
        """
    
        if not data:
            return
        
        url = self.url + 'api/sharefactory/test'

        t = threading.Thread(target=self.__Post, args=(url,data))
        t.start()

    def TransWeight(self,data):
        """
        异步同步称重数据，获取相关称重数据后调用，无需关系接收端是否保存成功
        参数：
            data：同步的数据
        返回值：
            字典对象：{'Code':200, 'Msg':'***', 'UserData':obj}
            Code:200表示调用成功，否则失败
            Msg:错误信息
            UserData:执行成功返回的数据
        """
    
        if not data:
            return {'Code':0, 'Msg':'参数验证失败'}

        url = self.url + 'api/sharefactory/test'

        return self.__Post(url, data)

