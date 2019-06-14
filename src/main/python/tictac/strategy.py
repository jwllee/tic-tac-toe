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
    'MinimaxStrategy'
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


class MinimaxStrategy(Strategy):
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
            minimax_v = self.minimax_r(board, 1, next_marker, marker)
            # minimax_v = self.minimax(board, next_marker, marker)
            if minimax_v > best_score:
                best_score = minimax_v
                best_move_loc = cell.loc
            board.unmark_cell(marker, cell.loc)

        took = time.time() - start
        self.logger.info('Took {:.2f}s for {} states'.format(took, self.n_explored_states))

        return best_move_loc

    def minimax_r(self, board, depth, cur_marker, marker):
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
            minimax_v = self.minimax_r(board, depth + 1, next_marker, marker)
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

    def minimax(self, board, cur_marker, marker):
        if board.state != BoardState.ONGOING:
            return self.utility(board, marker)

        # DFS with recurse back
        empty_cells = board.get_empty_cells()
        # np.random.shuffle(empty_cells)
        is_max = cur_marker == marker
        minimax = [-np.inf] if is_max else [np.inf]
        node_stack = [(
            None, # move that got to this state
            iter(empty_cells),
            minimax, # minimax value
            None, # marker for move
            cur_marker
        )]

        while node_stack:
            last_loc, children, minimax, last_marker, cur_marker = node_stack[-1]
            try:
                loc = next(children).loc
                board.mark_cell(cur_marker, loc)
                # self.logger.info('Marking {!r} for player "{!r}"'.format(loc, cur_marker))
                next_marker = Marker.next_marker(cur_marker)
                is_max = next_marker == marker
                minimax_1 = [-np.inf] if is_max else [np.inf]
                empty_cells = board.get_empty_cells()
                # np.random.shuffle(empty_cells)
                node = (
                    loc, iter(empty_cells), 
                    minimax_1, cur_marker, next_marker
                )
                node_stack.append(node)
            except:
                if board.state != BoardState.ONGOING:
                    # terminal state
                    utility = self.utility(board, marker)
                else:
                    utility = minimax[0]

                node_stack.pop(-1)

                if node_stack:
                    # update parent's minimax
                    is_max = last_marker == marker
                    parent = node_stack[-1]
                    if is_max:
                        parent[2][0] = max(parent[2][0], utility)
                    else:
                        parent[2][0] = min(parent[2][0], utility)
                    board.unmark_cell(last_marker, last_loc)
                    # self.logger.info('Unmarking {!r} for player "{!r}"'.format(last_loc, last_marker))
                else:
                    return utility
