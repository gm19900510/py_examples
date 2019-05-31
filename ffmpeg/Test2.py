# -*- coding:utf-8 -*-
import numpy as np
import subprocess
import cv2
import json
from multiprocessing import Process
 
ffmpeg_bin = 'C:/Users/Administrator/Desktop/EasyNVR-windows-3.0.0-1810081104/ffmpeg.exe '


def get_command(i, o):
    command = ffmpeg_bin + ' -i "' +  i + '" -vcodec copy  -f flv -an ' + o
    print(command)
    return command

 
def handle(i, o):
    p = subprocess.Popen(get_command(i, 'rtmp://192.168.3.56:1935/MyRed5/test' + o))
    print(p.pid) 
     
if __name__ == '__main__':
    array = [
            "rtsp://admin:admin12345@192.168.40.100/cam/realmonitor?channel=1&subtype=1"
            ]
    
    '''
    "rtsp://admin:admin12345@192.168.40.101/cam/realmonitor?channel=1&subtype=1",
            "rtsp://admin:admin12345@192.168.40.102/cam/realmonitor?channel=1&subtype=1",
            "rtsp://admin:admin12345@192.168.40.103/cam/realmonitor?channel=1&subtype=1",
            "rtsp://admin:admin12345@192.168.40.104/cam/realmonitor?channel=1&subtype=1",
            "rtsp://admin:admin12345@192.168.40.105/cam/realmonitor?channel=1&subtype=1"
            
            "rtsp://admin:admin12345@192.168.40.106/cam/realmonitor?channel=1&subtype=1",
            "rtsp://admin:admin12345@192.168.40.107/cam/realmonitor?channel=1&subtype=1",
            "rtsp://admin:admin12345@192.168.40.108/cam/realmonitor?channel=1&subtype=1",
            "rtsp://admin:admin12345@192.168.40.109/cam/realmonitor?channel=1&subtype=1"
    "rtsp://admin:hik12345@192.168.40.110/Streaming/Channels/1",
            "rtsp://admin:hik12345@192.168.40.111/Streaming/Channels/1",
            "rtsp://admin:hik12345@192.168.42.128/Streaming/Channels/1",
             "rtsp://admin:hik12345@192.168.42.142/Streaming/Channels/1",
             "rtsp://admin:hik12345@192.168.42.133/Streaming/Channels/1",
             "rtsp://admin:hik12345@192.168.42.145/Streaming/Channels/1",
             "rtsp://admin:hik12345@192.168.42.146/Streaming/Channels/1"
             "rtsp://admin:hik12345@192.168.3.160/Streaming/Channels/1"
    '''
    
    for idx, j in enumerate(array):
        c1 = Process(target=handle, args=(j, str(idx)))
        c1.start()
        #handle(j, str(idx))
    c1.join()
    
    #handle('rtsp://admin:hik12345@192.168.42.128/Streaming/Channels/1', '0')
