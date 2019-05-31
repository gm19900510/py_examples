# coding: utf-8
'''
用于测试视频帧读取放入队列，及队列读取写入本地
'''

import multiprocessing
import cv2
import json
import time
import datetime
from multiprocessing import Process, Queue

manager = multiprocessing.Manager()
q = Queue()

  
def consumer(pid, rtsp, classify, frame_count, q):
    print("开启消费序列进程", pid)
    cap = cv2.VideoCapture(rtsp)
    while True:
        success, frame = cap.read()
        if success:
            if frame_count % 25 == 0:
                start = datetime.datetime.now()
                q.put(frame)
                end = datetime.datetime.now()
                print(pid, '放入队列--------------->', (end - start))
            frame_count = frame_count + 1
            if frame_count > 10000:
                frame_count = 0


def main():
    json_array = '[{"cameraId":"0128","rtsp":"rtsp://admin:hik12345@192.168.42.128/Streaming/Channels/1"},{"cameraId":"0142","rtsp":"rtsp://admin:hik12345@192.168.42.142/Streaming/Channels/1"},{"cameraId":"0133","rtsp":"rtsp://admin:hik12345@192.168.42.133/Streaming/Channels/1"},{"cameraId":"0145","rtsp":"rtsp://admin:hik12345@192.168.42.145/Streaming/Channels/1"},{"cameraId":"0146","rtsp":"rtsp://admin:hik12345@192.168.42.146/Streaming/Channels/1"}]'
    array = json.loads(json_array)
    time.sleep(10)
    for i in array:
        c1 = Process(target=consumer, args=(i['cameraId'] , i['rtsp'], i['cameraId'], 0, q))
        c1.start()
    while True:
        frame = q.take()
        start = datetime.datetime.now()
        start = datetime.datetime.now()
        tmp_file_name = '%s.png' % str(datetime.datetime.now().strftime('%H%M%S%f'))
        cv2.imwrite('./recognition/detection/capture/panorama/' + tmp_file_name, frame, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        end = datetime.datetime.now()
        print('图片写入本地--------------->', (end - start))

 
if __name__ == '__main__':
    main()
