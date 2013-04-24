import socket
from lockfile import LockTimeout, AlreadyLocked
import time


class SocketLock(object):
    timeout = None
    lockname = None

    def __init__(self, lockname, timeout=None):
        #can't use super here as LinkFileLock is an old style class
        self.lockname = lockname
        self.timeout = timeout

    def acquire(self, timeout=None):
        if not timeout:
            timeout = self.timeout

        end_time = time.time()
        if timeout is not None and timeout > 0:
            end_time += timeout

        while True:
            try:
                self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                self.socket.bind('\0' + self.lockname)
                return
            except socket.error:
                if timeout is not None and time.time() > end_time:
                    if timeout > 0:
                        raise LockTimeout
                    else:
                        raise AlreadyLocked
                time.sleep(timeout is not None and timeout / 10 or 0.1)

    def release(self):
        self.socket.close()

    def __enter__(self):
        """
        Context manager support.
        """
        self.acquire()
        return self

    def __exit__(self, *_exc):
        """
        Context manager support.
        """
        self.release()
