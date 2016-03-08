import os, fcntl, errno

class Queue(object):
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
        w = self.pipe[1]
        os.write(w, '%s\n' % msg)
