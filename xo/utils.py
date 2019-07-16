from enum import Enum, IntEnum
import logging, logging.config


__all__ = [
    'make_logger',
    'assert_isinstance'
]


# set standard logging configurations
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(name)s] %(message)s'
        }
    },
    'handlers': {
        'standard': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['standard'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
})


def make_logger(name):
    return logging.getLogger(name)


def assert_isinstance(name, expected, actual):
    msg = """Class difference in {name}
             [expected]: {expected}
             [actual]: {actual}"""
    msg = msg.format(name=name,
                     expected=expected,
                     actual=actual)
    assert isinstance(actual, expected), msg