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
def do_work():
    pass

'''
Initialization:
    Initialize network queues
    Initialize logs
'''
def init_process(sockets, clock_speed):
    # initialize stuff 
    do_work()

'''
    Start 3 processes (threads?)
    Initialize network connections/listening on sockets
    Specify the number of clock ticks per second for each process (how often it should check msgs/send msgs)
'''
def main():
    init_process(sockets, clock_speed)

if __name__ == "__main__":
    main()
