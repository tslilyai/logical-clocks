import time
import random 
import sys

class Process(object):

    '''
    Initialization:
        Initialize network queues
        Initialize logs
    '''
    def __init__(self, proc_num, queues, clock_speed):
        # trial number
        self.trial_num = int(sys.argv[1])
        # number of possible types of events
        self.num_events = int(sys.argv[2])
        self.proc_num = proc_num
        self.msg_queues = queues
        self.my_queue = queues[proc_num]
        self.clock_speed = clock_speed
        self.log = "logs/%d-events-%d:%d.log" % (proc_num, self.trial_num, self.num_events)
        # clear out the old logs
        f = open(self.log, 'w')
        f.write("Clock Speed: %d\n" % self.clock_speed)
        f.close()
        self.lc = 0
     
    def run_process(self):
        while True:
            time.sleep((1.0/self.clock_speed))
            self.do_work()
            
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
        self.lc += 1

        if not self.my_queue.empty():
            self.lc = max(self.lc, int(self.my_queue.get()))
            event_tpe = "Receive"
            with open(self.log, 'a') as f:
                f.write("Event: %s\tGlobal Time: %s\tMsgQueue Length: %d\tLC: %d\n" % 
                        (event_tpe, global_time, self.my_queue.qsize(), self.lc))
        else:
            event = random.randint(1,self.num_events)
            if event == 1:
                recipient = (self.proc_num + 1) % 3
                event_tpe = "Send to VM %d" % recipient
                self.msg_queues[recipient].put(self.lc)
            elif event == 2:
                recipient = (self.proc_num + 2) % 3
                event_tpe = "Send to VM %d" % recipient
                self.msg_queues[recipient].put(self.lc)
            elif event == 3:
                recipients = [(self.proc_num + 1) % 3,(self.proc_num + 2) % 3]
                event_tpe = "Send to VMs %d and %d" % (recipients[0], recipients[1])
                self.msg_queues[recipients[0]].put(self.lc)
                self.msg_queues[recipients[1]].put(self.lc)
            else:
                event_tpe = "Internal Event"

            with open(self.log, 'a') as f:
                f.write("Event: %s\tGlobal Time: %s\tLC: %d\n" % 
                        (event_tpe, global_time, self.lc))
