from abc import ABC, abstractmethod
import numpy as np
import time, sys

from xo import utils
from xo.board.utils import *
from xo.strategy.utils import *


LOGGER = utils.make_logger(__file__)


__all__ = [
    'Strategy',
    'RandomStrategy',
]


class Strategy(ABC):
    def __init__(self, strategy_type):
        self.strategy_type = strategy_type
        self.logger = utils.make_logger(Strategy.__name__)

    @abstractmethod
    def get_move(self, board, marker):
        raise NotImplementedError('Please implement this method.')

    def save_data(self):
        pass


class RandomStrategy(Strategy):
    def __init__(self):
        super().__init__(StrategyType.RANDOM)

    def get_move(self, board, marker):
        empty_cells = board.get_empty_cells()
        n_cells = len(empty_cells)
        if n_cells <= 0:
            raise ValueError('No empty cells available to choose!')
        ind = np.random.choice(range(n_cells), size=None)
        cell = empty_cells[ind]
        return cell.loc
