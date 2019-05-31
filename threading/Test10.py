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


def do(i, filelist):  
    with open("F://机器学习内容备份//hik-facecapture-service//Picture//" + str(filelist[i]), 'rb') as f:  # 以二进制读取图片
        data = f.read()
        encodestr = base64.b64encode(data)  # 得到 byte 编码的数据
        encodestr = str(encodestr, encoding="utf8")  
        
        postdata = {
          "limit": 0,
          "ranges": [
            {
              "photoAlbumId": "f1eb1ec5-9ac1-471b-8750-e3d7c63ddfd8"
            }
          ],
          "searchMode": "AUTO",
          "targets": [
            {
              "photoData": encodestr
            }
          ],
          "threshold": 0
        }
    postdata = json.dumps(postdata) 
    
    print(postdata) 
    
    r = requests.post('http://192.168.3.209:8080/v4/query/search', data=postdata, headers=headers)
    print(r.text)
    end = datetime.datetime.now()
    print(end - start)


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
for i in range(1):  # 创建100个线程
    t = threading.Thread(target=do, args=(i, filelist))
    t.start()
 
time.sleep(10000)
