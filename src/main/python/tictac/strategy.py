from abc import ABC, abstractmethod
from enum import Enum
from . import utils
import numpy as np


LOGGER = utils.make_logger(utils.LoggerType.MINIMAL.name)


__all__ = [
    'StrategyType',
    'RandomStrategy',
    'MinimaxStrategy'
]


class StrategyType(Enum):
    RANDOM = 1
    MINIMAX = 2


class Strategy(ABC):
    def __init__(self, strategy_type):
        self.strategy_type = strategy_type

    @abstractmethod
    def get_move(self, board):
        raise NotImplementedError('Please implement this method.')


class RandomStrategy(Strategy):
    def __init__(self):
        super().__init__(StrategyType.RANDOM)

    def get_move(self, board):
        empty_cells = board.get_empty_cells()
        n_cells = len(empty_cells)
        if n_cells <= 0:
            raise ValueError('No empty cells available to choose!')
        ind = np.random.choice(range(n_cells), size=None)
        cell = empty_cells[ind]
        return cell.loc


class MinimaxStrategy(Strategy):
    def __init__(self):
        super().__init__(StrategyType.MINIMAX)
