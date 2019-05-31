# -*- coding: utf-8 -*-
def quicksort(array): 
    # 基线条件：为空或只包含一个元素的数组是“有序”的
    if len(array) < 2: 
        return array 
    else: 
        pivot = array[0]  # 递归条件
        
        less = [i for i in array[1:] if i <= pivot]  # 由所有小于基准值的元素组成的子数组
        
        greater = [i for i in array[1:] if i > pivot]  # 由所有大于基准值的元素组成的子数组
        
        return quicksort(less) + [pivot] + quicksort(greater)  # 小于大于基准值的子数组重新递归


print (quicksort([10, 5, 2, 3]))
