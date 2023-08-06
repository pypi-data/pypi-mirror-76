
import time


def print_time_consuming(func):
    def inner(*args, **kwargs):
        start = time.time()
        results = func(*args, **kwargs)
        end = time.time()
        time_consuming = end - start
        print("Time consuming:", time_consuming)
        return results
    return inner
