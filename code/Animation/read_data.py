from multiprocessing import Process, Queue
import time, random
from multiprocessing import freeze_support


# 写数据进程执行的代码:
def write(qc, ql):
    L = [30, 35, 40]
    C = [100, 110, 120]
    # while True: 
    for left, center in zip(L, C):
        qc.put(center)
        ql.put(left)
        time.sleep(random.random())

# 读数据进程执行的代码:
def read(qc, ql):
    while True:
        center = qc.get(True)
        left = ql.get(True)

def run():
    # 父进程创建Queue，并传给各个子进程：
    qc = Queue()
    ql = Queue()
    pw = Process(target=write, args=(qc, ql))
    pr = Process(target=read, args=(qc, ql))
    # 启动子进程pw，写入:
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()

def main():
    freeze_support()
    run()