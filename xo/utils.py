from enum import Enum, IntEnum
import logging, logging.config


__all__ = [
    'make_logger',
    'assert_isinstance',
    'NotificationType',
    'NotificationKey'
]


class NotificationType(IntEnum):
    CELL = 1
    STATE = 2
    MESSAGE = 3
    PROMPT_MOVE = 4
    BOARD_UPDATE = 5
    GAME_END = 6


class NotificationKey(IntEnum):
    CELL = 1
    STATE = 2
    BOARD = 3
    MESSAGE = 4
    MARKER = 5
    PLAYER = 6


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
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        }
    },
    'loggers': {
        '': {
            'handlers': ['standard'],
            'level': 'INFO',
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
