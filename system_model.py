import sys
import time
import random 
import thread

'''
If there is a message in the message queue for the machine:
    take one message off the queue
    update the local logical clock
    log: 
        received a message
        the global time (gotten from the system)
        the length of the message queue
        the logical clock time.

If there is no message in the queue,generate a random number in the range of 1-10:
    1: send to one of the other machines a message that is the local logical clock time
    2: send to the other virtual machine a message that is the local logical clock time.
    3: send to both of the other virtual machines a message that is the logical clock time
    Other than 1-3: treat the cycle as an internal event
    *For all events:
        Update the local logical clock
        Log the event, the system time, and the logical clock value
'''
def do_work(f):
    event = random.randint(1,10)
    f.write("Event: %s\tGlobal Time: %s\tMsgQueue Length: %d\tLC Time: %s\n" % 
            (event_tpe, global_time, queue_len, lc_time))

'''
Initialization:
    Initialize network queues
    Initialize logs
'''
def init_process(proc_num, sockets, clock_speed):
    # initialize stuff 
    try:
        with open("%d-events.log" % proc_num, 'w') as f:
            while(1):
                sleep(clock_speed)
                do_work(f)
    except KeyboardInterrupt:
        sys.exit()

'''
    Start 3 processes (threads?)
    Initialize network connections/listening on sockets
    Specify the number of clock ticks per second for each process (how often it should check msgs/send msgs)
        Random number between 1 and 6
'''
def main():
    #sockets = 
    for i in range(3):
        clock_speed = random.randint(1,6)
        init_process(i, sockets, clock_speed)

if __name__ == "__main__":
    main()
