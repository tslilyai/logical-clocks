import time
import random 
import sys
import math

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
        # should we collect metrics or not
        self.collect_metrics = bool(sys.argv[3])
        self.proc_num = proc_num
        self.msg_queues = queues
        self.my_queue = queues[proc_num]
        self.clock_speed = clock_speed
        self.log = "logs/%d-events-%d:%d.log" % (proc_num, self.trial_num, self.num_events)
        # clear out the old logs
        f = open(self.log, 'w')
        f.write("Clock Speed: %d\n" % self.clock_speed)
        f.close()

        if self.collect_metrics:
            self.metrics = "metrics/%d-events-%d:%d.log" % (proc_num, self.trial_num, self.num_events)
            f = open(self.log, 'w')
            f.write("Clock Speed: %d\n" % self.clock_speed)
            f.close()
        self.lc = 0
     
    def run_process(self):
        if self.collect_metrics:
            self.num_jumps = 0
            self.jumps = []
            self.queue_sizes = []
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
       
        # save the old lc
        if self.collect_metrics:
            old_lc = self.lc
        
        self.lc += 1
        if not self.my_queue.empty():
            
            queue_sz = self.my_queue.qsize()
            event_tpe = "Receive"
            self.lc = max(self.lc, int(self.my_queue.get()))
            
            with open(self.log, 'a') as f:
                f.write("Event: %s\tGlobal Time: %s\tMsgQueue Length: %d\tLC: %d\n" % 
                        (event_tpe, global_time, queue_sz, self.lc))            
           
            # update averages
            if self.collect_metrics:
                self.jumps.append(float(self.lc-old_lc))
                self.queue_sizes.append(float(queue_sz))
                (jump_data, q_data) = (get_metrics(self.jumps), get_metrics(self.queue_sizes))
                with open(self.metrics, 'a') as f:
                    f.write("LC Jump Avg: %f\tLC Jump SD: %f\n" % jump_data)
                    f.write("Q Length Avg: %f\tQ Length SD: %f\n\n" % q_data)
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

def get_metrics(data):
    s0 = len(data)
    s1 = sum(data)
    s2 = sum(x*x for x in data)
    mean = s1 / s0
    if s0 > 1:
        std_dev = math.sqrt((s0*s2 - s1*s1) / (s0*(s0-1)))
    else:
        std_dev = 0
    return (mean, std_dev)
