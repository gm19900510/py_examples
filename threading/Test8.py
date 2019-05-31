# coding:utf-8

import threading
import time
event = threading.Event()


def service():
    print('开启服务')
    event.wait()  # 括号里可以带数字执行，数字表示等待的秒数，不带数字表示一直阻塞状态
    print('服务开启成功')


def start():
    time.sleep(3)
    print('开始执行业务')
    time.sleep(3)
    event.set()  # 默认为False，set一次表示True，所以子线程里的foo函数解除阻塞状态继续执行


def conn():
    while True:
        if event.is_set() == False:
            print('数据库连接成功')
            time.sleep(1)
            event.set()
            event.wait()
            break
        

t = threading.Thread(target=service, args=())  # 子线程执行foo函数
t.start()
t2 = threading.Thread(target=start, args=())  # 子线程执行start函数
t2.start()
t3 = threading.Thread(target=conn, args=())  # 子线程执行do函数
t3.start()
