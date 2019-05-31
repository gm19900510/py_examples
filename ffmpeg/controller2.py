# -*- coding:utf-8 -*-
import subprocess
import time 
import argparse
import redis
import sys
import codecs
import paho.mqtt.client as mqtt
import traceback
from multiprocessing import Process

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())


def handle(ffmpeg_path, input_path, out_path):
    command = [ffmpeg_path , '-i' , input_path , '-vcodec', 'copy', '-f' , 'flv', '-an' , out_path]
    p = subprocess.Popen(command)
    return p


def transcoding(ffmpeg_path, rtmp_path, device, device_id, process_id, redis_host):
    pool = redis.ConnectionPool(host=redis_host)  # 实现一个连接池
    r = redis.Redis(connection_pool=pool)  
    
    # 子进程PID键值不存在表示无转换码流进行，需进行转换
    if not r.exists(process_id):
        print('用户执行播放操作，无转换进程，开启转换进程') 
        # 获取设备的RTSP路径
        rtsp_path = str(r.get(device_id), encoding="utf-8")
        print('设备：' + device_id + ' ，对应的RTSP路径：', rtsp_path) 
           
        p = handle(ffmpeg_path, rtsp_path, rtmp_path + device)
        print('开始执行码流转换进程：' , p.pid) 
       
        print('保存码流转换进程键值对：' + process_id, 1) 
        r.setex(process_id, 60 * 60 * 3, 1)
      
        while True:
            time.sleep(20)
            if not r.exists(process_id):
                p.kill()
                print('码流转换进程键值对不存在，关闭转换进程') 
                break; 
        sys.exit(0)    
    # 子进程PID键值存在表示有转换码流进行，运行进程数+1
    else:
        process_num = int(str(r.get(process_id), encoding="utf-8"))
        print('用户执行播放操作，存在转换进程，当前转换进程数：', process_num) 
        r.setex(process_id, 60 * 60 * 1, (process_num + 1))
        print('更新码流转换进程键值对：' + process_id, (process_num + 1)) 
        sys.exit(0)


# 消息处理函数
def on_message_come(mqttClient, userdata, msg): 
    try :
        topic = msg.topic
        device = msg.payload.decode("utf-8")
        
        device_id = 'device_id_' + device
        process_id = 'process_id_' + device
    
        print(topic)
        print('device_id：', device_id)
        print('process_id：', process_id)
        
        if topic == 'ffmpeg/play':
            c1 = Process(target=transcoding, args=(args.ffmpeg_path, args.rtmp_path, device, device_id, process_id, args.redis_host))
            c1.start()
        
        elif topic == 'ffmpeg/play_done':
            if r.exists(process_id): 
                process_num = int(str(r.get(process_id), encoding="utf-8"))
                print('用户执行播放停止操作，存在转换进程，当前转换进程数：', process_num) 
                if process_num == 1:
                    print('删除码流转换进程键值对：' + process_id)  
                    r.delete(process_id)
                else:    
                    r.setex(process_id, 60 * 60 * 3, (process_num - 1)) 
                    print('更新码流转换进程键值对：' + process_id, (process_num - 1))  
            else:
                print('流转换进程键值对不存在') 
            # sys.exit(0)       
        
    except Exception as e:
        print('traceback.print_exc():', traceback.print_exc(), e)  
         
    return     


def on_subscribe():
    mqttClient.subscribe("ffmpeg/play", 1)  # 主题为"ffmpeg/play"
    mqttClient.subscribe("ffmpeg/play_done", 1)  # 主题为"ffmpeg/play_done"
    
    mqttClient.on_message = on_message_come  # 消息到来处理函数
    return

     
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='controller')
    parser.add_argument("-ffmpeg_path", "--ffmpeg_path", default='C:/Users/Administrator/Desktop/EasyNVR-windows-3.0.0-1810081104/ffmpeg.exe', help='path to ffmpeg.')
    parser.add_argument("-rtmp_path", "--rtmp_path", default='rtmp://192.168.3.56:1935/live/', help='path to rtmp.')
    parser.add_argument('-mqtt_host', '--mqtt_host', default='192.168.3.202', help='')
    parser.add_argument('-mqtt_port', '--mqtt_port', default=1883, help='')
    parser.add_argument('-redis_host', '--redis_host', default='192.168.3.56', help='')
    
    args = parser.parse_args()
    
    mqttClient = mqtt.Client() 
    # mqttClient.will_set("", "", 1, True)  # 设置遗嘱消息
    mqttClient.connect(args.mqtt_host, args.mqtt_port, 60)
    mqttClient.loop_start()
    
    pool = redis.ConnectionPool(host=args.redis_host)  # 实现一个连接池
    r = redis.Redis(connection_pool=pool)  
    
    on_subscribe()
    print('服务开启')   
    
    while True:
        pass;
