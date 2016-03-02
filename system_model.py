from process import Process
import random 
import thread

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
        sockets = []
        p = Process(i, sockets, clock_speed)
        thread.start_new_thread(p.run_process,())

if __name__ == "__main__":
    main()
