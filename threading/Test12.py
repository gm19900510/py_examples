# -*- coding: utf-8 -*-
import threading
import datetime
import requests
import time
import base64
import json
# 人脸比对检索并发性能测试工具

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Content-Type':'application/json'
}


def do():  
    while True:
        r = requests.get('http://192.168.3.209:8080/v4/subscriptions/devAlertTopic/messages?maxWaitTimeSeconds=1&maxMessages=5', headers=headers)
        print(r.text)
        r = requests.get('http://192.168.3.209:8080/v4/subscriptions/devStateChangeTopic/messages?maxWaitTimeSeconds=1&maxMessages=5', headers=headers)
        print(r.text)



do()