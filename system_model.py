import sys
import time
import random 
from process import Process

'''
    Start 3 processes (threads?)
    Initialize network connections/listening on sockets
    Specify the number of clock ticks per second for each process (how often it should check msgs/send msgs)
        Random number between 1 and 6
'''
def main():
    # TODO
    #sockets = 
    for i in range(3):
        clock_speed = random.randint(1,6)
        p = Process(i, sockets, clock_speed)
        p.run_process()

if __name__ == "__main__":
    main()
