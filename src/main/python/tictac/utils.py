from enum import Enum
import logging, logging.config


__all__ = [
    'FormatType',
    'HandlerType',
    'LoggerType'
]


class FormatType(Enum):
    STANDARD = 1
    MINIMAL = 2


class HandlerType(Enum):
    DEFAULT = 1
    MINIMAL = 2


class LoggerType(Enum):
    DEFAULT = 1
    MINIMAL = 2


# set standard logging configurations
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        FormatType.STANDARD.name: {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        FormatType.MINIMAL.name: {
            'format': '%(message)s'
        }
    },
    'handlers': {
        HandlerType.DEFAULT.name: {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': FormatType.STANDARD.name
        },
        HandlerType.MINIMAL.name: {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': FormatType.MINIMAL.name
        },
    },
    'loggers': {
        LoggerType.DEFAULT.name: {
            'handlers': [HandlerType.DEFAULT.name],
            'level': 'INFO',
            'propagate': True
        },
        LoggerType.MINIMAL.name: {
            'handlers': [HandlerType.MINIMAL.name],
            'level': 'DEBUG',
            'propagate': True
        },
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
