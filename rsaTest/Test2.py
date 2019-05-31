#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wmi
import json
import rsa
import base64

c = wmi.WMI()

with open('public.pem', "rb") as publickfile:
    p = publickfile.read()
    pubkey = rsa.PublicKey.load_pkcs1(p)
    print(pubkey)
with open('private.pem', "rb") as privatefile:
    p = privatefile.read()
    privkey = rsa.PrivateKey.load_pkcs1(p)
    print(privkey)


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
    with open('sys.info', 'w') as f:  # 设置文件对象
        crypto = rsa.encrypt(json.dumps(getCpuId()).encode('utf-8'), privkey)
        crypto64 = base64.b64encode(crypto)
        f.write(str(crypto64, encoding="utf8") + "\n")       
        crypto = rsa.encrypt(json.dumps(getBaseboardSerialnumber()).encode('utf-8'), pubkey)  
        crypto64 = base64.b64encode(crypto)       
        f.write(str(crypto64, encoding="utf8")) 
        
   
    with open('sys.info', 'r') as f1:
        list = f1.readlines()
        for i in range(0, len(list)):
            list[i] = list[i].rstrip('\n')
            crypto = base64.b64decode(list[i])
            message = rsa.decrypt(crypto, privkey)
            message = str(message, encoding="utf8")
            print(message)  

      
if __name__ == '__main__':
    main()
