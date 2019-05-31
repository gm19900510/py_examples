# coding: utf-8
'''
用于测试视频帧读取放入队列，及队列读取写入本地
'''

import cv2

  
def consumer():
    cap = cv2.VideoCapture('camera_test1.avi')
    frame_count = cap.get(7)    #获取视频总帧数
    fps = cap.get(5)    #获取视频帧率
    print(frame_count)
    print(fps)
    while cap.isOpened():
        isSuccess, frame = cap.read()
        if isSuccess: 
            print(cap.get(0),cap.get(2))

def main():
    consumer()

 
if __name__ == '__main__':
    main()
