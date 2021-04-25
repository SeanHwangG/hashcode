import logging
import pathlib
import glob
import contextlib
import functools
import time
import signal
from typing import List
from line_profiler import LineProfiler

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s, %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
class timeout(contextlib.ContextDecorator):
    def __init__(self, seconds, *, timeout_message=os.strerror(errno.ETIME), suppress_error=False):
        self.seconds = seconds
        self.timeout_message = timeout_message
        self.suppress_error = suppress_error

    def _timeout_handler(self, signum, frame):
        raise TimeoutError(self.timeout_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self._timeout_handler)
        signal.alarm(self.seconds)

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)
        if self.suppress_error and exc_type is TimeoutError:
            return True


def parse_input(file_name: str):
    with open(file_name, "r") as f:
        pass
    return

def to_output(file_name: str):
    with open(file_name, 'w') as f:
        f.write(f"ab")
    return

def main():
    for fn in glob.glob('input/*'):
        logging.info(f"{fn}")
        _ = parse_input(fn)
        to_output("out_filename")

if __name__ == "__main__":
    lp = LineProfiler()
    lp_wrapper = lp(main)
    try:
        with timeout(10):
            lp_wrapper()
    finally:
        lp.print_stats()