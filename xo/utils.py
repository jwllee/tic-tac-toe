import time


def timeit(func):
    def timed(*args, **kwargs):
        start = time.time()
        results = func(*args, **kwargs)
        end = time.time()
        took = end - start
        info_msg = '{} took {:.3f}s'
        info_msg = info_msg.format(func.__name__, took)
        print(info_msg)
        return results
    return timed
