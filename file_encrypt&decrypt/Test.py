# -* -coding: UTF-8 -* -
'''
异或方式对文件进行加密和解密
'''

import os
import datetime


# 主函数
def main():
    getInput()


# 输入参数
def getInput():

    # 获取操作的参数
    while(True):

        oper = input("请输入操作(e:加密 d:解密):")

        if(oper == "e" or oper == "d"):
            break
        else:
            print("输入有误，请重新输入!")

    # 获取文件密码
    while(True):

        password = input("请输入密码:")
    
        if(len(password) == 0):
            print("密码不能为空!")
        else:
            break

    # 获取操作的文件路径
    while(True):

        path = input("请输入文件路径（示例：C:\\test.txt）:")

        try:
            f_read = open(path, "rb")
        except:
            print("文件没有找到，请检查路径是否存在！")
        else:
            break

    # 进行加密或解密操作
    if(oper == "e"):
        encrypt(path, password)
    elif(oper == "d"):
        decrypt(path, password)


# 加密
def encrypt(path, password):
    start = datetime.datetime.now()
    # 因为刚学可能有库可以直接获取这些信息吧，不过自己写个算法获取这些信息也没什么难度
    fileFullName = path.split(os.path.sep)  # os.path.sep为操作系统的文件分隔符
    fileName = fileFullName[len(fileFullName) - 1].split(".")[0]
    fileSuffix = fileFullName[len(fileFullName) - 1].split(".")[1]

    # print("文件全名称:",fileFullName[len(fileFullName)-1])
    # print("文件名称:",fileName)
    # print("文件后缀:",fileSuffix)

    fileParent = path[0:len(path) - len(fileFullName[len(fileFullName) - 1])]
    newFileName = "加密_" + fileFullName[len(fileFullName) - 1]
    newFilePath = fileParent + newFileName

    # print("文件父路径:",fileParent)
    # print("新的文件名称:",newFileName)
    # print("新的文件全路径:", newFilePath)

    f_read = open(path, "rb")
    f_write = open(newFilePath, "wb")

    count = 0  # 当前密码加密索引

    # 我们采用异或循环加密
    for now in f_read:  # 通过迭代器逐行访问
        for nowByte in now:  # 通过迭代器逐字符处理
            newByte = nowByte ^ ord(password[count % len(password)])
            count += 1
            f_write.write(bytes([newByte]))

    f_read.close()
    f_write.close()
    
    end = datetime.datetime.now()
    print("文件加密完毕^_^", (end - start))


# 解密（因为我们采取的异或解密，所以其实和加密算法一样）
def decrypt(path, password):
    start = datetime.datetime.now()
    fileFullName = path.split(os.path.sep)  # os.path.sep为操作系统的文件分隔符
    fileName = fileFullName[len(fileFullName) - 1].split(".")[0]
    fileSuffix = fileFullName[len(fileFullName) - 1].split(".")[1]

    # print("文件全名称:", fileFullName[len(fileFullName)-1])
    # print("文件名称:", fileName)
    # print("文件后缀:", fileSuffix)

    fileParent = path[0:len(path) - len(fileFullName[len(fileFullName) - 1])]
    newFileName = "解密_" + fileFullName[len(fileFullName) - 1]
    newFilePath = fileParent + newFileName

    # print("文件父路径:", fileParent)
    # print("新的文件名称:", newFileName)
    # print("新的文件全路径:", newFilePath)

    f_read = open(path, "rb")
    f_write = open(newFilePath, "wb")

    count = 0  # 当前密码加密索引

    # 我们采用异或循环加密
    for now in f_read:  # 通过迭代器逐行访问
        for nowByte in now:  # 通过迭代器逐字符处理
            newByte = nowByte ^ ord(password[count % len(password)])
            count += 1
            f_write.write(bytes([newByte]))

    f_read.close()
    f_write.close()
    end = datetime.datetime.now()
    print("文件解密完毕", (end - start))


main()
