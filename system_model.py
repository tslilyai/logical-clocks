from process import Process
from queue import Queue
import random 
import threading
import time

import os
import sys

'''
    Start 3 VMs (i.e. "Process" threads)
    Initialize network connections (i.e. array of message queues)
    Specify the number of clock ticks per second for each process (how often it should check msgs/send msgs)
        Random number between 1 and 6
'''
def main():
    if len(sys.argv) != 4:
        print "Usage: python system_model [trial_number] [num_possible_events] [collect_metrics(true/false)]"
    msg_queues = [Queue() for _ in range(3)]
    threads = []
    pids = []
    for i in range(3):
        clock_speed = random.randint(1,6)
        p = Process(i, msg_queues, (clock_speed))
        pid = os.fork()
        if pid == 0:
            p.run_process()
        elif pid < 0:
            print 'Fork error'
            sys.exit(1)
        else:
            pids.append(pid)

    for pid in pids:
        os.waitpid(pid, 0)

if __name__ == "__main__":
    main()
