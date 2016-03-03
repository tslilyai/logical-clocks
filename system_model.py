from process import Process
from Queue import Queue
import random 
import threading
import time

'''
    Start 3 VMs (i.e. "Process" threads)
    Initialize network connections (i.e. array of message queues)
    Specify the number of clock ticks per second for each process (how often it should check msgs/send msgs)
        Random number between 1 and 6
'''
def main():
    msg_queues = [Queue() for _ in range(3)]
    threads = []
    run_event = threading.Event()
    run_event.set()
    for i in range(3):
        clock_speed = random.randint(1,6)
        p = Process(i, msg_queues, clock_speed, run_event)
        threads.append(threading.Thread(target=p.run_process))
    for t in threads:
        t.start()
        print "started thread!"

    try:
        while 1:
            time.sleep(.1)
    except:
        run_event.clear()
        print 'Killing threads. Please wait.'
        for t in threads:
            t.join()

if __name__ == "__main__":
    main()
