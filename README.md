# logical-clocks

David Ding and Lily Tsai

Usage: `python system_model [trial_number] [collect_metrics(true/false)] [probability of a send]`
- trial_number is used to uniquely identify the log files produced
- collect_metrics can be set to true to collect metrics on logical clock values and queue length
- P(send) must be between 0 and 1 and sets how likely a machine will send messages

`collect_metrics.sh` simulates the model for one minute for some number of trials with differing probabilities of a send.

`analyze.py` can be used to collect drift statistics from log files

## Model Design
An asynchronous distributed system typically consists of several machines which communicate via some type of network connection. Each of these machines may run at a different clock speed. In this assignment, we model a small, asynchronous distributed system on a single machine by using processes as abstractions for each separate machine. 

Each process has a Unix pipe to simulate its network connection.
Other processes can send a message to a certain process by writing to that process's pipe,
and the process could read messages send to it by reading from the pipe.
All writes and reads are done
with the `write`
and `read` system calls directly
to avoid buffering by system IO libraries.
Messages in our system are delimited
by newlines ('\\n'),
and are sent by a single `write` system
call to the write end of the pipe;
writes of size less than `PIPE_BUF`
are guaranteed to be atomic by the POSIX standard.
We assert that all messages sent are have length less than `PIPE_BUF`.
To read, we read one character
at a time from the pipe,
which is guaranteed to return the
characters in the order that they were written.
We read as much data as possible
from the pipe until the pipe becomes empty, and store the read characters in an internal buffer.
We set the flags of the read end of the pipe to be `O_NONBLOCK` via the fcntl function call;
reads are then guaranteed to be nonblocking,
and if the pipe is empty,
the read call returns immediately,
setting `errno` to be `EWOULDBLOCK`.
When this happens, we store whatever partial message we may have read, and immediately return;
the partial messages is not considered to be fully received until we receive the newline marking the end of the message.

We have a nifty abstraction for the pipe following the same interface as the Python Queue class, with methods such as put and get
to retrieve messages from the queue.
We create each Queue in the original
spawning daemon, with all the pipes
opened.
We then call `fork` n times,
where n is the number of machines.
Because of the semantics of `fork`,
these Queues all live in different address spaces and share no internal state;
however, the file descriptors
corresponding to the pipes
all refer to the same underlying object in the operating system,
allowing other processes to write
to a pipe and have
the Queue's designed owner read these messages.

## Model Behavior
To simulate how one machine sends a network message to another, we append the sender's message to the receiving machine's queue. To simulate a machine's clock speed, we specify an integer n between 1 and 6; this integer then corresponds to the number of events per second on a machine (i.e. the number clock cycles per second). Each machine enters an infinite loop. In each iteration, the machine first sleeps for 1/n seconds, then simulates one cycle of the model system. 

In both the real and model systems, a typical mechanism for ordering events within the system is a logical clock. At every clock cycle, a machine m partakes in some type of event---either external or internal---that updates its logical clock as follows:

1. Increment LC(m). This ensures that LC(m) is unique per event.

2. If there is a message in m's queue, m takes the message off the queue and updates its logical clock to be the maximum of the sender's logical clock value and its own. The sender's logical cock value is contained within the received message.

3. Otherwise, we do one of the following:
    -  Send machine m+1 the value LC(m) with probability 10%
    -  Send machine m+2 the value LC(m) with probability 10%
    -  Send machines m+1 and m+2 the value LC(m) with probability 10%
    -  If none of the above events are triggered, generate an internal event.

