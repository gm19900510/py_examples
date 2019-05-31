# -*- coding:utf-8 -*-
import redis
import subprocess
import time 
import sys


def handle(ffmpeg_path, input_path, out_path):
    command = [ffmpeg_path , '-i' , input_path , '-vcodec', 'copy', '-f' , 'flv', '-an' , out_path]
    p = subprocess.Popen(command)
    return p


class TranscodeTool(): 

    def __init__(self, args): 
        self.pool = redis.ConnectionPool(host=args.redis_host)  # 实现一个连接池
        self.r = redis.Redis(connection_pool=self.pool) 
        self.args = args
    
    def trans(self, device):
        device_id = 'device_id_' + device
        process_id = 'process_id_' + device
        print('device_id：', device_id)
        print('process_id：', process_id)
        
        # 子进程PID键值不存在表示无转换码流进行，需进行转换
        if not self.r.exists(process_id):
            print('用户执行播放操作，无转换进程，开启转换进程') 
            # 获取设备的RTSP路径
            rtsp_path = str(self.r.get(device_id), encoding="utf-8")
            print('设备：' + device_id + ' ，对应的RTSP路径：', rtsp_path) 
               
            p = handle(self.args.ffmpeg_path, rtsp_path, self.args.rtmp_path + device)
            print('开始执行码流转换进程：' , p.pid) 
           
            print('保存码流转换进程键值对：' + process_id, 1) 
            self.r.setex(process_id, 60 * 60 * 1, 1)
          
            while True:
                time.sleep(20)
                if not self.r.exists(process_id):
                    p.kill()
                    print('码流转换进程键值对不存在，关闭转换进程') 
                    break; 
            sys.exit(0)    
        
        else:  # 子进程PID键值存在表示有转换码流进行，运行进程数+1
            process_num = int(str(self.r.get(process_id), encoding="utf-8"))
            print('用户执行播放操作，存在转换进程，当前转换进程数：', process_num) 
            self.r.setex(process_id, 60 * 60 * 1, (process_num + 1))
            print('更新码流转换进程键值对：' + process_id, (process_num + 1)) 
            sys.exit(0)
