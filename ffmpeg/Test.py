# -*- coding:utf-8 -*-
import os, sys, getopt
import numpy as np
import subprocess as sp
import cv2
 
# command line parser
'''
try:
    opts, args = getopt.getopt(sys.argv[1:], "i:s:",["help"])
except getopt.GetoptError:
    sys.exit()
for op, value in opts:
    if op == "-i":
        input_file = value
    elif op== "-s":
        widthheight = value.split('*')
        width = np.int(widthheight[0])
        height = np.int(widthheight[1])
'''
input_file = 'rtsp://admin:hik12345@192.168.3.160/Streaming/Channels/1'
width = 704
height = 576
 
# videoIO
FFMPEG_BIN = "E:/ffmpeg-20180227-fa0c9d6-win64-static/bin/ffmpeg.exe"
command_in = [ FFMPEG_BIN,
            '-i', input_file,
            '-f', 'rawvideo',
            '-s', str(width) + '*' + str(height),
            '-pix_fmt', 'bgr24',
            '-']
pipe_in = sp.Popen(command_in, stdout=sp.PIPE)
 
command_out = ['C:/Users/Administrator/Desktop/EasyNVR-windows-3.0.0-1810081104/ffmpeg.exe',
    '-y',
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', str(width) + '*' + str(height),
    # '-r', str(fps),
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    # '-preset', 'ultrafast',
    # '-acodec', 'copy',
    # '-vcodec', 'copy',
    '-f', 'flv',
    'rtmp://192.168.3.56:1935/MyRed5/test']
 
pipe_out = sp.Popen(command_out, stdin=sp.PIPE)  # ,shell=False
 
 
# 这是处理每一帧图像的函数
def process(img):
    cv2.imshow('image', img)
 
 
# read width*height*3 bytes (= 1 frame)
while True:
    raw_image = pipe_in.stdout.read(width * height * 3)
    image = np.fromstring(raw_image, dtype='uint8')
    if(len(image) == 0):
        break
    image = image.reshape((height, width, 3)).copy()
    process(image)
    # sys.stdout.write(image.tostring())
    # pipe_in.stdout.flush()
    pipe_out.stdin.write(image.tostring())  # 存入管道  
    pipe_out.stdin.flush()
    k = cv2.waitKey(1)  
    # q键退出
    if (k & 0xff == ord('q')):  
        break  