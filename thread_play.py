from Queue import Queue
from threading import Thread
import threading
from uuid import uuid4
import time


def main():

    q2 = Queue()

    iterations = 10
    count = 0
    t1 = Thread(target=generator, args=(count, iterations, q2))
    t1.start()
    print("Thread Active Count {}".format(threading.activeCount()))
    t2 = Thread(target=consumer, args=(q2,))
    t2.start()
    q2.join()


def generator(count, iterations, q2):
    print threading.currentThread()
    while count != iterations:
        for idx, item in enumerate(range(20)):
            uu_id = uuid4()
            q2.put((count, idx, uu_id))
            time.sleep(.1)
        count += 1


def consumer(q2):
    print threading.activeCount()
    while True:
        try:
            count, idx, uu_id = q2.get(block=True, timeout=5)
            print count, idx, uu_id
            q2.task_done()
        except Exception as e:
            if e.message == '':
                break
if __name__ == "__main__":
    main()
