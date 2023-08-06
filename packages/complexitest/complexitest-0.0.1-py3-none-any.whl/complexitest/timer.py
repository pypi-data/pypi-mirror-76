# Code from: https://www.jujens.eu/posts/en/2018/Jun/02/python-timeout-function/
import signal
import gc
from time import time
from contextlib import contextmanager


@contextmanager
def timeout(seconds):
    '''
    time in seconds
    '''
    # Register a function to raise a TimeoutError on the signal.
    signal.signal(signal.SIGALRM, raise_timeout)
    # Schedule the signal to be sent after ``time``.
    signal.setitimer(signal.ITIMER_REAL, seconds)

    try:
        yield
    except TimeoutError:
        raise TimeoutError
    finally:
        # Unregister the signal so it won't be triggered
        # if the timeout is not reached.
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, signal.SIG_IGN)


def raise_timeout(signum, frame):
    raise TimeoutError


class Timer:
    def __init__(self):
        self.elapsed = None
        self.start = None

    def __enter__(self):
        gc.disable()
        self.start = time()

    def __exit__(self, exception_type, exception_value, traceback):
        self.elapsed = time() - self.start
        gc.enable()
