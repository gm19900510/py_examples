# -*- coding: utf-8 -*-
'''
计算100W级别欧式距离及相识度的运行时间
'''
import numpy as np
import datetime

if __name__ == '__main__':

    start = datetime.datetime.now()
    faces = []
    face = np.random.randn(512)
    for i in range(0, 1000000): 
        arry = np.random.randn(512)
        faces.append(np.array(arry))
    
    end = datetime.datetime.now()
    print('生成1000000数组--->', (end - start))
   
    start = datetime.datetime.now()
    dists = []
    for i in range(0, 1000000): 
        dist = np.sum(np.square(face - faces[i]))
        dist = np.sqrt(dist)
        dists.append(dist)
        # print(dist) 
    
    end = datetime.datetime.now()
    print('比较1000000数组的欧式距离--->', (end - start))
        
    index = np.argsort(dists)  # from small to large
    
    end = datetime.datetime.now()
    print('比较1000000数组的欧式距离排序--->', (end - start))
    
    
    for i in range(0, 10):
        #print('欧式距离--->', dists[index[i]]) 
        sim = np.dot(faces[index[i]], face)
        print('相识度--->', sim)
    
    end = datetime.datetime.now()
    print('计算前十的相识度--->', (end - start))
