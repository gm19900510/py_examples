# -*- coding: utf-8 -*-
'''
Created on 2019年3月6日

@author: Administrator
'''
import sqlite3
import numpy as np
import json

# 创建数据库连接对象
conn = sqlite3.connect('sample_database.db', isolation_level=None)  # 连接到SQLite数据库
'''
参数isolation_level是同Conection.isolation_level的属性意义一样
'''
# 参数:memory:来创建一个内存数据库
# conn = sqlite3.connect(":memory:", isolation_level=None)

x = np.arange(12).reshape(2, 6)

# conn = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()
# 删除数据库表
cursor.execute("DROP TABLE test2")
# 创建数据库表
cursor.execute("create table test2 (arr BLOB)")
# 插入一行数据,numpy.array转List,json.dumps()函数是将字典转化为字符串
cursor.execute("insert into test2 (arr) values (?)", (json.dumps(x.tolist()),))
# 提交
conn.commit()

cursor.execute("select arr from test2")
data = cursor.fetchall()

print(data)
print(type(data))

# json.loads()函数是将字符串转化为字典
my_list = json.loads(data[0][0])
# List转numpy.array
temp = np.array(my_list)
print(temp)
print(type(temp))

cursor.close()  # 关闭Cursor
conn.close()  # 关闭数据库
