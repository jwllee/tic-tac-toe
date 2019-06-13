from abc import ABC, abstractmethod
from enum import Enum
from . import utils
from .board import *
import numpy as np
import time


LOGGER = utils.make_logger(utils.LoggerType.MINIMAL.name)


__all__ = [
    'StrategyType',
    'RandomStrategy',
    'MinimaxStrategy2p'
]


class StrategyType(Enum):
    RANDOM = 1
    MINIMAX = 2


class Strategy(ABC):
    def __init__(self, strategy_type):
        self.strategy_type = strategy_type
        self.logger = utils.make_logger(Strategy.__name__)

    @abstractmethod
    def get_move(self, board, marker):
        raise NotImplementedError('Please implement this method.')


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


class MinimaxStrategy2p(Strategy):
    def __init__(self):
        super().__init__(StrategyType.MINIMAX)
        self.best_move_loc = None
        self.n_explored_states = 0

    def get_move(self, board, marker):
        copy = board.copy(include_observers=False)
        self.n_explored_states = 0
        return self.get_best_move(copy, marker)

    def get_max_score(self, board):
        # max score is the max depth + 1 of the game tree
        # max depth is just the number of cells in board
        return board.n_cells + 1

    def utility(self, board, marker):
        max_score = self.get_max_score(board)
        if board.is_winner(marker):
            return max_score
        elif board.has_winner:
            return -max_score
        else: # either draw or ongoing
            return 0

    def get_best_move(self, board, marker):
        empty_cells = board.get_empty_cells()
        next_marker = Marker.next_marker(marker)
        best_move_loc = None
        best_score = -np.inf

        start = time.time()

        for cell in empty_cells:
            board.mark_cell(marker, cell.loc)
            # self.logger.info('Marked {!r} for player "{!r}"'.format(cell.loc, marker))
            minimax_v = self.minimax(board, 1, next_marker, marker)
            if minimax_v > best_score:
                best_score = minimax_v
                best_move_loc = cell.loc
            board.unmark_cell(marker, cell.loc)

        took = time.time() - start
        self.logger.info('Took {:.2f}s for {} states'.format(took, self.n_explored_states))

        return best_move_loc

    def minimax(self, board, depth, cur_marker, marker):
        self.n_explored_states += 1
        # if self.n_explored_states % 5000 == 0:
        #     self.logger.info('Explored {} states'.format(self.n_explored_states))

        score = self.utility(board, marker)

        max_score = self.get_max_score(board)
        if score == max_score:
            return score

        if score == -max_score:
            return score

        if board.full:
            return 0

        is_max = cur_marker == marker
        empty_cells = board.get_empty_cells()
        next_marker = Marker.next_marker(cur_marker)
        best_score = -np.inf if is_max else np.inf

        for cell in empty_cells:
            board.mark_cell(cur_marker, cell.loc)
            minimax_v = self.minimax(board, depth + 1, next_marker, marker)
            aux = best_score
            if is_max:
                best_score = max(best_score, minimax_v)
            else:
                best_score = min(best_score, minimax_v)

            if aux != best_score:
                # update best move loc
                self.best_move_loc = cell.loc

            board.unmark_cell(cur_marker, cell.loc)

        return best_score
