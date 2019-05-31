import multiprocessing

# Value/Array
def func1(a, arr):
    a.value = 3.14
    for i in range(len(arr)):
        arr[i] = 0
    a.value = 0

if __name__ == '__main__':
    num = multiprocessing.Value('d', 1.0)  # num=0
    arr = multiprocessing.Array('i', range(10))  # arr=range(10)
    p = multiprocessing.Process(target=func1, args=(num, arr))
    p.start()
    p.join()
    print (num.value)
    print (arr[:])
