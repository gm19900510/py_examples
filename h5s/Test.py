# coding: utf-8
from urllib import parse, request
import json
import threading
import os
import datetime
import ftplib
import shutil
import time

ftp_host = '192.168.3.104'
ftp_username = 'zyfw'
ftp_password = '@wsx1qaz'

url = "http://192.168.3.68:8080/"
textmod = {'user':'admin', 'password':'12345'}
textmod = parse.urlencode(textmod)
filepath = "C://"
record_time = 10.0

# 输出内容:user=admin&password=admin
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko'}
requert_url = url + 'api/v1/Login'
# 登录操作
req = request.Request(url='%s%s%s' % (requert_url, '?', textmod), headers=header_dict)
res = request.urlopen(req)
res = res.read()
print(res.decode(encoding='utf-8'))
# 输出内容:登录成功
j_res = json.loads(res)
strSession = j_res['strSession']
print(strSession)

# 获取录像设备
requert_url = url + 'api/v1/GetSrc'
req = request.Request(url=requert_url)
res = request.urlopen(req)
res = res.read()
print(res.decode(encoding='utf-8'))
j_res = json.loads(res)
strToken = j_res['src'][0]['strToken']
print(strToken)

# 开始初始录像
textmod = {'token':strToken, 'session':strSession}
textmod = parse.urlencode(textmod)
requert_url = url + 'api/v1/ManualRecordStart'
print(requert_url)
# 登录操作
req = request.Request(url='%s%s%s' % (requert_url, '?', textmod), headers=header_dict)
res = request.urlopen(req)
res = res.read()
print(res.decode(encoding='utf-8'))


def record(strSession, strToken):
    print(strSession, strToken)
    
    # 结束录像
    requert_url = url + 'api/v1/ManualRecordStop'
    req = request.Request(url='%s%s%s' % (requert_url, '?', textmod), headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    print(res.decode(encoding='utf-8'))
   
    # 重新开始录像
    requert_url = url + 'api/v1/ManualRecordStart'
    req = request.Request(url='%s%s%s' % (requert_url, '?', textmod), headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    print(res.decode(encoding='utf-8'))

    t = threading.Thread(target=file_upload, args=())
    t.start()
    
    global timer
    timer = threading.Timer(record_time, record, [strSession, strToken])
    timer.start()


def file_upload():
    time.sleep(2)
    ospath = filepath + strToken + "//" + datetime.datetime.now().strftime('%Y-%m-%d') + 'TZ08'
    dir_list = get_file_list(ospath)
    if dir_list:
        for d in dir_list:
            c = os.listdir(ospath + "//" + d)
           
            if c:  # 判断文件夹是否为空                
                l = searchFile(ospath + "//" + d)  
                print(l)
                if l:
                    fileFullName = l[0].split("\\")
                    fileName = fileFullName[len(fileFullName) - 1]   
                    print(fileName)
                    
                    f = ftplib.FTP(ftp_host)  # 实例化FTP对象
                    f.login(ftp_username, ftp_password)  # 登录
                    # 获取当前路径
                    pwd_path = f.pwd()
                    print("FTP当前路径:", pwd_path)
                    ftp_upload(f, fileName, l[0])
                    
                    print(ospath + "//" + d)
                    try:
                        shutil.rmtree(ospath + "//" + d)
                    except: 
                        print()
                        
                    break 
                  
            else:
                try:
                    os.rmdir(ospath + "//" + d)
                except: 
                    print()
                
                
               
def ftp_upload(f, file_remote, file_local):
    '''以二进制形式上传文件'''
    # file_remote = 'ftp_upload.txt'
    # file_local = 'D:\\test_data\\ftp_upload.txt'
    bufsize = 1024  # 设置缓冲器大小
    fp = open(file_local, 'rb')
    f.storbinary('STOR ' + file_remote, fp, bufsize)
    fp.close()
        

def searchFile(start_dir, target=['.mp4']):
    os.chdir(start_dir);   
    py_list = [];
    for each_file in  os.listdir(os.curdir):
        ext = os.path.splitext(each_file)[1]
        if ext in target:
            py_list.append(str(os.getcwd() + os.sep + each_file))
        if os.path.isdir(each_file):
            searchFile(each_file, target);
            os.chdir(os.pardir)      
    return py_list         

            
def get_file_list(file_path):
    dir_list = os.listdir(file_path)
   
    if not dir_list:
        return
    else:
        # 注意，这里使用lambda表达式，将文件按照最后修改时间顺序升序排列
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        #dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        dir_list = dir_list.sort()
        # print(dir_list)
        return dir_list
    


if __name__ == "__main__":
    timer = threading.Timer(record_time, record, [strSession, strToken])
    timer.start()
