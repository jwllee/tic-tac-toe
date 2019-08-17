import time
import logging, logging.config


logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        },
    }
})


def make_logger(name):
    return logging.getLogger(name)


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
