from enum import Enum
from . import utils


LOGGER = utils.make_logger(utils.LoggerType.MINIMAL.name)


__all__ = [
    'StrategyType'
]


class StrategyType(Enum):
    RANDOM = 1
    MINIMAX = 2


def get_move_random(board_state):
    return None


def get_move_minimax(board_state):
    return None
