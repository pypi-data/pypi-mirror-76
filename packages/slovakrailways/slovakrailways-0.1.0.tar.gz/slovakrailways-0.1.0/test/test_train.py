
import sys
import time
import unittest
import warnings

sys.path.append(".")

import slovakrailways as zsr

def delay_test(timeout = 1):
    def time_sleep_decorator(fn):
        def replace_time_sleep(*args, **kw):
            time.sleep(timeout)
            return fn(*args, **kw)
        return replace_time_sleep
    return time_sleep_decorator

class TestTrain(unittest.TestCase):
    def setUp(self):
        pass
        
    @delay_test(timeout = 1)
    def test_track_train(self):
        x = zsr.track_train("609")
        
        

__all__ = ["TestTrain"]