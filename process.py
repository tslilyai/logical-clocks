import sys
import time
import random 
import thread


def Process():

    '''
    Initialization:
        Initialize network queues
        Initialize logs
    '''
    def __init__(self, proc_num, sockets, clock_speed):
        self.proc_num = proc_num
        self.clock_speed = clock_speed
        # TODO add sending functionality (i.e. sockets/pipes) 
        self.sockets = sockets
        self.log = "%d-events.log" % proc_num
        self.msg_queue = []
        self.lc = 0
     
    def run_process(self):
        try:
            while(1):
                time.sleep(clock_speed)
                self.do_work()
        except KeyboardInterrupt:
            sys.exit()    
            
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
    def do_work(self):
        global_time = time.time()

        if len(msg_queue) != 0:
            self.lc = max(self.lc, msg_queue.pop(0))
            event_tpe = "Receive"
            with open(self.log, 'rw') as f:
                f.write("Event: %s\tGlobal Time: %s\tMsgQueue Length: %d\tLC: %d\n" % 
                        (event_tpe, global_time, len(msg_queue), self.lc))
        
        # TODO add sending functionality (i.e. sockets/pipes) 
        else:
            event = random.randint(1,10)
            if event == 1:
                recipient = (proc_num + 1) % 3
                event_tpe = "Send to VM %d" % recipient
            elif event == 2:
                recipient = (proc_num + 2) % 3
                event_tpe = "Send to VM %d" % recipient
            elif event == 3:
                recipients = [(proc_num + 1) % 3,(proc_num + 2) % 3]
                event_tpe = "Send to VMs %d and %d" % (recipients[0], recipients[1])
            else:
                event_tpe = "Internal Event"
                self.lc += 1
            with open(self.log, 'rw') as f:
                f.write("Event: %s\tGlobal Time: %s\tLC: %d\n" % 
                        (event_tpe, global_time, self.lc))


