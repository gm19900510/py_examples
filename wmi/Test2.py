#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wmi
import json
c = wmi.WMI()


# 处理器
def getCpuId():
    cpus = []
    for cpu in c.Win32_Processor():
        tmpdict = {}     
        tmpdict["ID"] = cpu.ProcessorId.strip()
        cpus.append(tmpdict)
    print(cpus)    
    return cpus


# 主板
def getBaseboardSerialnumber():
    boards = []
    for board_id in c.Win32_BaseBoard():
        tmpmsg = {}
        tmpmsg['Serial Number'] = board_id.SerialNumber  # 主板序列号
        boards.append(tmpmsg)
    print(boards)
    return boards


def main():
    with open('sys.info','w') as f:    #设置文件对象
        f.write(json.dumps(getCpuId())+'\n')                 #将字符串写入文件中
        f.write(json.dumps(getBaseboardSerialnumber()))
   
   
    with open('sys.info', 'r') as f1:
        list = f1.readlines()
        for i in range(0, len(list)):
            list[i] = list[i].rstrip('\n')
            print(list[i])  
      
if __name__ == '__main__':
    main()
