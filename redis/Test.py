# -*- coding:utf-8 -*-

import redis


     
if __name__ == '__main__':

    pool = redis.ConnectionPool(host='192.168.3.56')  # 实现一个连接池
    r = redis.Redis(connection_pool=pool)  
    
    #r.set('device_id_test', "rtsp://admin:hik12345@192.168.3.160/Streaming/Channels/1") 
    rtsp_path = str(r.get("device_1e554b3d-a458-4316-b1a3-6e04108f11bb"), encoding="utf-8")
    print(rtsp_path)