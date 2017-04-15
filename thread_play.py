from Queue import Queue
from threading import Thread
import threading
from uuid import uuid4
import time

# This is written for python 2.7.x.  This is to simulate putting items into a DB via a REST API with one thread and then
# verify the data was inserted into the DB with another thread running in parallel to the generate thread.


def main():

    q2 = Queue()

    iterations = 10
    count = 0

    # Instatiate the first thread and pass in the reference to the queue
    t1 = Thread(target=generator, args=(count, iterations, q2))
    # Start the thread generating data
    t1.start()

    # This shows us the number of threads running.  It should be two right now.
    # One for the main thread and one for our t1 thread
    print("Thread Active Count {}".format(threading.activeCount()))

    # We now start a second thread to consume the data that thread 1 is putting in the queue
    # If you are confused at the extra comma after q2 in args, its a requirement if you have only
    # one item.
    t2 = Thread(target=consumer, args=(q2,))
    t2.start()

    # We print our active threads which should now be 3, one for main thread, one for t1 and one for t2
    print("Thread Active Count {}".format(threading.activeCount()))

    q2.join()


def generator(count, iterations, q2):
    print threading.currentThread()
    while count != iterations:
        for idx, item in enumerate(range(20)):
            # We create a unique identifier with uuid4()
            uu_id = uuid4()

            # When we put items in the queue, be sure to use double (()) or it will trigger exception
            q2.put((count, idx, uu_id))

            # We put a sleep in here so we force t1 to be slower at generating data than t2 is at consuming it.
            time.sleep(.1)
        count += 1


def consumer(q2):
    print threading.currentThread()
    while True:
        try:
            # We get an item out of the queue. The key factor here is the block and timeout params.
            # As t1 is producing data slower because of its sleep, we need this thread to wait on data to fill the queue
            # t2 though will always be checking for something to enter the queue, but after 5 seconds of nothing in the queu
            # it will timeout and throw and "Empty" exception.
            count, idx, uu_id = q2.get(block=True, timeout=5)

            print("Iteration: {} Range: {} Unique ID: {}".format(count, idx, uu_id))

            # We tell the queue that the last item we got out of it has been processed.
            q2.task_done()
        except Exception as e:
            # We the queue has remained empty for 5 seconds, we break out of our while True loop
            if e.message == '':
                break
if __name__ == "__main__":
    main()
