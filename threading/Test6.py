# coding:utf-8

import time
import threading
 
semaphore = threading.Semaphore(3)

 
def func():
    if semaphore.acquire():
        print (threading.currentThread().getName() + '获取锁')
        time.sleep(5) 
        semaphore.release()
        print (threading.currentThread().getName() + '释放锁')
 
 
for i in range(10):
    t1 = threading.Thread(target=func)
    t1.start()
