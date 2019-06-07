'''
thread target function, 檢查queue中是否還有工作需處理
'''
import threading
import time


def ConsumeQueue(*args):
    queue = args[0]
    lock = args[1]
    ThdId = args[2]

    while True:
        if queue.qsize() >0:
            job = queue.get()
            lock.release()
            job.setThdId(ThdId)
            job.do()
        else:
            lock.release()
            break

def launch_thread(que, queLock, num):
    thd = []
    for i in range(num+1):
        thd_obj = threading.Thread(target=ConsumeQueue, name='Thd'+str(i), args=(que, queLock, i))
        thd_obj.start()
        thd.append(thd_obj)

        for i in range(num+1):
            while thd[i].is_alive():
                time.sleep(5)