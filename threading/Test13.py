# -*- coding: utf-8 -*-
import threading
import datetime
import requests
import time
import paho.mqtt.client as mqtt
import base64
import json
import random
# 人脸比对检索并发性能测试工具

MQTTHOST = "192.168.3.202"
MQTTPORT = 1883
mqttClient = mqtt.Client()

# 连接MQTT服务器
def on_mqtt_connect():
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()


# 订阅相关主题
def on_subscribe():
    mqttClient.subscribe("face/compare/#", 1) 
    mqttClient.subscribe("face/hit/+", 1)
    mqttClient.subscribe("eyesight/webface/hit/+", 1)
    mqttClient.subscribe("face/search/#", 1)
    mqttClient.subscribe("face/detection/#", 1)
    mqttClient.subscribe("eyesight/face/location/+", 1)
    mqttClient.on_message = on_message_come  # 消息到来处理函数


# 接受结果处理
def on_message_come(mqttClient, userdata, msg): 
    print("产生消息", msg.payload.decode("utf-8"))
    end = datetime.datetime.now()
    print(end - start)


headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Content-Type':'application/json'
}

on_mqtt_connect() 
on_subscribe()


def do(i, filelist):  
    with open("F://机器学习内容备份//hik-facecapture-service//Picture//" + str(filelist[i]), 'rb') as f:  # 以二进制读取图片
        data = f.read()
        encodestr = base64.b64encode(data)  # 得到 byte 编码的数据
        encodestr = str(encodestr, encoding="utf8")  
       
        nowstr = datetime.datetime.now().strftime('%H%M%S%f')
        requestId = str(random.randrange(0, 10001, 5)) + '_%s' % str(nowstr)
        postdata = {
          "requestId":requestId,
          "deviceId": "0",
          "time": "0",
          "data": encodestr
        }
    postdata = json.dumps(postdata) 
    
    #print(postdata) 
    r = requests.post('http://192.168.3.209:7070/location/face', data=postdata, headers=headers)
    #print(r.text)
    #end = datetime.datetime.now()
    #print(end - start)


import os  


def file_name(file_dir):   
    L = []   
    for root, dirs, files in os.walk(file_dir):  
        for file in files:  
            if os.path.splitext(file)[1] == '.jpg' or os.path.splitext(file)[1] == '.png':  
                L.append(file)  
    return L 


filelist = file_name("F://机器学习内容备份//hik-facecapture-service//Picture")

print(filelist)

# 获取线程执行开始时间
start = datetime.datetime.now()
for i in range(500):  # 创建100个线程
    t = threading.Thread(target=do, args=(i, filelist))
    t.start()
 
time.sleep(10000)
