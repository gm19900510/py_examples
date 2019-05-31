# -*- coding: utf-8 -*-
import threading
import datetime
import paho.mqtt.client as mqtt
import time
import random
# 人脸比对检索并发性能测试工具

MQTTHOST = "192.168.41.249"
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


def do(i,filelist):
    # mqttClient.publish('face/compare', '{"fileNames":"1552903547277.jpg,1552903553605.jpg","requestId":"12312312"}', 1, False)
    #mqttClient.publish('face/detection', '{"fileName":"1551343618268.jpg","requestId":"50d615a2-82d8-4eb8-930d-9c2db834f44b"}', 1, False)
    nowstr = datetime.datetime.now().strftime('%H%M%S%f')
    face_file_name = str(random.randrange(0, 10001, 5)) + '_face_%s.jpg' % str(nowstr)
    #print(face_file_name)
    print(filelist[i])
    
    mqttClient.publish('eyesight/webface/hit', '{"fileName":"'+face_file_name+'","requestId":"50d615a2-82d8-4eb8-930d-9c2db834f44b","fileUrlPath":"http://192.168.3.56:8080/'+filelist[i]+'"}', 1, False)
    
    # mqttClient.publish('eyesight/face/location', '{"deviceId":"deviceId_'+str(i)+'","fileName":"'+face_file_name+'","requestId":"50d615a2-82d8-4eb8-930d-9c2db834f44b","fileUrlPath":"http://192.168.3.56:8080/'+filelist[i]+'"}', 1, False)

    
    #1551343618268.jpg 1551405713510.jpg
    #mqttClient.publish('face/hit', '{"fileName":"'+filelist[i]+'","requestId":"50d615a2-82d8-4eb8-930d-9c2db834f44b"}', 1, False)
    #end = datetime.datetime.now()
    #print('------>', end - start)

import os  
def file_name(file_dir):   
    L=[]   
    for root, dirs, files in os.walk(file_dir):  
        for file in files:  
            if os.path.splitext(file)[1] == '.jpg' or os.path.splitext(file)[1] == '.png':  
                L.append(file)  
    return L 

filelist = file_name("D://apache-tomcat-8.0.33//webapps//ROOT")

print(filelist)

on_mqtt_connect() 
on_subscribe()

#33.74

#rnet100
#方式一：人脸检测、人脸识别占用同四块显卡
#CUDA_VISIBLE_DEVICES=0,1,2,3 python eyesight_face_service_v006_gpu.py -tta -u -c -s -ed 
#1进程 1000并发  1张人脸  43.06耗时
#1进程 1000并发 2张人脸1:13.60耗时

#4进程 1000并发  1张人脸  41.15耗时
#4进程 1000并发 2张人脸1:16.82耗时

#--------------------------------
#方式二：人脸检测、人脸识别占用同一块显卡
#不指定运行的显卡
#1进程 1000并发  1张人脸  44.83耗时
#1进程 1000并发 2张人脸 1:14.25耗时

#方式二：人脸检测占用一块显卡，人脸识别占用一块显卡
#mtcnn不指定，mx.gpu(1)
#1进程 1000并发  1张人脸  46.24耗时

#方式三：人脸检测占用一块显卡，人脸识别占用四块显卡
#mtcnn不指定，mx.gpu(gpuid)
#4进程 1000并发  1张人脸  19.36耗时
#4进程 1000并发 2张人脸 30.12耗时

#--------------------------------
#4进程 1000并发  1张人脸  19.09耗时
#4进程 1000并发 2张人脸 29.67耗时

#8进程 1000并发  1张人脸  16.46耗时
#8进程 1000并发 2张人脸 26.32耗时

#12进程 1000并发  1张人脸  16.72耗时
#12进程 1000并发 2张人脸 24.67耗时

#16进程 1000并发  1张人脸  16.35耗时
#16进程 1000并发 2张人脸 23.81耗时

#20进程 1000并发  1张人脸  15.22耗时
#20进程 1000并发 2张人脸 22.20耗时

#rnet50
#4进程 1000并发  1张人脸  15.38耗时
#4进程 1000并发 2张人脸 21.68耗时

#8进程 1000并发  1张人脸  12.53耗时
#8进程 1000并发 2张人脸 17.97耗时

#12进程 1000并发  1张人脸  12.43耗时
#12进程 1000并发 2张人脸  18.02耗时

#16进程 1000并发  1张人脸  11.92耗时
#16进程 1000并发 2张人脸 17.57耗时



#获取线程执行开始时间
start = datetime.datetime.now()
for i in range(500):  # 创建100个线程
    t = threading.Thread(target=do, args=(i,filelist))
    t.start()
 
time.sleep(10000)
