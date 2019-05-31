#encoding: utf-8
'''
收集主机的信息：
主机名称、IP、系统版本、服务器厂商、型号、序列号、CPU信息、内存信息
'''

import subprocess
import os,sys
import uuid

''' 获取 ifconfig 命令的输出 '''
def getMac():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

''' 获取Linux系统主机名称 '''
def getHostname():
    p = subprocess.Popen(['uname -s -r -m -n'], shell = True, stdin=subprocess.PIPE, stdout=subprocess.PIPE ,stderr=subprocess.PIPE)
    data = p.stdout.read().decode('utf-8')
    return {'hostname':data}

if __name__ == '__main__':
    #getHostname()
    print(getMac())
    
    
    