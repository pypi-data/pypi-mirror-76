#coding:utf-8

import sys
import json
import requests
import threading


class LocalPushHelper:
    def __init__(self,url):
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

    def PushWeightAsync(self, data):
        if not data:
            return {'Code':0, 'Msg':'参数验证失败'}

        url = self.url + 'push'

        try:

            t = threading.Thread(target=self.__Post, args=(url,data))
            t.start()
        except Exception as e:
            pass

    def PushWeight(self,data):
        """
        称重数据调用本地服务推送客户端
        参数：
            data：推送的数据
        返回值：
            1：成功
            -1：失败
        """
    
        if not data:
            return {'Code':0, 'Msg':'参数验证失败'}

        url = self.url + 'push'

        return self.__Post(url, data)

    def KillWeightProgram(self):

        url = self.url + 'kill'

        self.__Post(url)

