import os, fcntl, errno, select

class Queue(object):
    '''
        An inter-process queue that uses the same interface as the Python Queue.Queue class.

        Internally, the queue uses a pipe for processes to communicate.
        Queue elements are separated by new lines.
        Reading from the pipe is done in a non-blocking way.

        To use this Queue class, create a Queue object before fork.
        Then, both processes, though their queue copies live in separate address spaces,
        share a pipe through which they could communicate.
    '''
    def __init__(self):
        self.pipe = os.pipe()
        fcntl.fcntl(self.pipe[0], fcntl.F_SETFL, os.O_NONBLOCK)
        self.buf = []
        self._ibuf = []

    def __del__(self):
        os.close(self.pipe[0])
        os.close(self.pipe[1])

    def get(self):
        self._fetch_many()
        return self.buf.pop(0)
    
    # Reads as many elements from the pipe, not blocking on failure
    def _fetch_many(self):
        r = self.pipe[0]
        while True:
            try:
                c = os.read(r, 1)
            except OSError as e:
                # Nothing to read
                if e.errno == errno.EWOULDBLOCK:
                    return
                raise e
            if c == '\n':
                self.buf.append(''.join(self._ibuf))
                self._ibuf = []
            elif c == '':
                return
            else:
                self._ibuf.append(c)

    def qsize(self):
        self._fetch_many()
        return len(self.buf)

    def empty(self):
        self._fetch_many()
        if self.buf:
            return False
        return True

    def put(self, msg):
        assert len('%s\n' % msg) < select.PIPE_BUF
        w = self.pipe[1]
        os.write(w, '%s\n' % msg)
