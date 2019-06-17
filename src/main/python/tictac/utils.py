from enum import Enum, IntEnum
import logging, logging.config


__all__ = [
    'FormatType',
    'HandlerType',
    'LoggerType', 
    'NotificationType',
    'NotificationKey'
]


class NotificationType(IntEnum):
    MESSAGE = 1
    STATE = 2
    PLAYER_MOVE = 3


class NotificationKey(IntEnum):
    MESSAGE = 1
    STATE = 2
    MARKER = 3
    PLAYER = 4


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
        'Game': {
            'handlers': [HandlerType.DEFAULT.name],
            'level': 'DEBUG',
            'propagate': True
        },
        'Board': {
            'handlers': [HandlerType.DEFAULT.name],
            'level': 'DEBUG',
            'propagate': True
        },
        'View': {
            'handlers': [HandlerType.DEFAULT.name],
            'level': 'DEBUG',
            'propagate': True
        },
        'Strategy': {
            'handlers': [HandlerType.DEFAULT.name],
            'level': 'DEBUG',
            'propagate': True
        },
        'MainWindow': {
            'handlers': [HandlerType.DEFAULT.name],
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
