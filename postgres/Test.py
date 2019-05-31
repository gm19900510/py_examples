# -*- coding: utf-8 -*-
import psycopg2
import numpy as np
import json


def insertOperate():
    conn = psycopg2.connect(database="openfire", user="postgres", password="postgres", host="192.168.3.202", port="5432")
    cursor = conn.cursor()
    x = np.arange(12).reshape(2, 6)
    # 建表
    cursor.execute('create table insightface.t_test ("data" bytea)')

    insert_sql = "insert into insightface.t_test (\"data\") values ('%s')"
    insert_sql = insert_sql % json.dumps(x.tolist())
    print(insert_sql)
    # 插入
    cursor.execute(insert_sql)
    # 提交
    conn.commit() 
    cursor.close()  # 关闭Cursor
    conn.close()  # 关闭数据库


def selectOperate():
    conn = psycopg2.connect(database="openfire", user="postgres", password="postgres", host="192.168.3.202", port="5432")
    cursor = conn.cursor()
    cursor.execute("select data from insightface.t_test")
    rows = cursor.fetchall()
    for row in rows:
        print (row[0], '\n')
        print(type(row[0]))
        print(bytes.decode(bytes(row[0])))
        print(type(bytes.decode(bytes(row[0]))))
        my_list = json.loads(bytes.decode(bytes(row[0])))
        # List转numpy.array
        temp = np.array(my_list)
        print(type(temp))
        print(temp.shape)
        print(temp)
        
    conn.close()

    
if __name__ == '__main__':
    insertOperate()
    selectOperate()
