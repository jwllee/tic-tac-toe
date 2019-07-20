from abc import ABC, abstractmethod
from enum import Enum
import numpy as np
import time, sys, pickle

from xo import utils
from xo.utils import *
from xo.board.utils import *
from xo.strategy.base import *
from xo.strategy.utils import *


LOGGER = make_logger(__file__)


__all__ = [
    'MinimaxStrategy'
]


class StateCacheKey:
    def __init__(self, board_v, is_max):
        self.board_v = board_v
        self.is_max = is_max

    def __hash__(self):
        # assume 32-bit builds, 1 bit is used for sign since hash is an integer
        ravel = self.board_v.ravel()
        hash_ = addition_hash(ravel, ravel.shape[0])
        hash_ = (hash_ * 19) + self.is_max
        return int(hash_)

    def __eq__(self, other):
        if not isinstance(other, StateCacheKey):
            return False
        return hash(other) == hash(self)

    def __reduce_(self):
        return (StateCacheKey, (self.board_v, self.is_max))


class MinimaxStrategy(Strategy):
    def __init__(self, cache_fp, prune=True, cache=True, table=dict()):
        super().__init__(StrategyType.MINIMAX)
        self.logger = make_logger(MinimaxStrategy.__name__)
        self.cache_fp = cache_fp
        self.best_move_loc = None
        self.n_explored_states = 0
        self.n_pruned = 0
        self.prune = prune
        self.cache = cache
        self.transposition_table = table

    def save_data(self):
        self.logger.info('Saving transposition table')
        with open(self.cache_fp, 'wb') as f:
            pickle.dump(self.transposition_table, f,
                        protocol=pickle.HIGHEST_PROTOCOL)
    
    def get_move(self, board, marker):
        copy = board.copy(register_observers=False)
        self.n_explored_states = 0
        self.n_pruned = 0
        start = time.time()
        move = self.get_best_move(copy, marker)
        end = time.time()
        took = end - start
        print('Move took: {:.3f}s'.format(took))
        return move

    def get_max_score(self, board):
        # max score is the max depth + 1 of the game tree
        # max depth is just the number of cells in board
        return board.n_cells + 1

    def utility(self, board, marker, depth=0):
        max_score = self.get_max_score(board)
        if board.is_winner(marker):
            return max_score - depth
        elif board.has_winner:
            return -(max_score - depth)
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
            self.logger.debug('Marked {!r} for player "{!r}"'.format(cell.loc, marker))
            minimax_v = self.minimax(board, next_marker, marker)
            if minimax_v > best_score:
                best_score = minimax_v
                best_move_loc = cell.loc
            board.unmark_cell(marker, cell.loc)

        took = time.time() - start
        # self.logger.info('Took {:.2f}s for {} states'.format(took, self.n_explored_states))
        table_size = sys.getsizeof(self.transposition_table)
        # self.logger.info('Transposition table size: {:.0f}b'.format(table_size))

        return best_move_loc

    def pruneable(self, node_stack, minimax, is_max):
        if len(node_stack) > 1 and self.prune:
            # self.logger.info('List length: {}'.format(len(node_stack)))
            parent = node_stack[-2]
            minimax_p = parent[3]
            lower_larger_than_par_upper = is_max and minimax[0] > minimax_p[1]
            upper_less_than_par_lower = not is_max and minimax[1] < minimax_p[0]

            if lower_larger_than_par_upper or upper_less_than_par_lower:
                # self.logger.info('Pruned {!r} for player "{!r}"'.format(last_loc, last_marker))
                # can prune this state without looking at child
                self.n_pruned += 1
                if self.n_pruned % 1000 == 0:
                    self.logger.info('Pruned {} states'.format(self.n_pruned))
                children.clear()
                return True
        return False

    def minimax(self, board, cur_marker, marker):
        if board.state != BoardState.ONGOING:
            return self.utility(board, marker)

        # DFS with recurse back
        empty_cells = board.get_empty_cells()
        # np.random.shuffle(empty_cells)
        is_max = cur_marker == marker
        # minimax = [-np.inf] if is_max else [np.inf]
        minimax = [-np.inf, np.inf]
        node_stack = [(
            0, # depth
            None, # move that got to this state
            empty_cells,
            minimax, # minimax value
            None, # marker for move
            cur_marker
        )]

        while node_stack:
            # start = time.time()
            depth, last_loc, children, minimax, last_marker, cur_marker = node_stack[-1]

            try:
                loc = children.pop(0).loc
                # has children, decide whether if we can prune this state
                is_max = last_marker == marker
                if self.pruneable(node_stack, minimax, is_max):
                    continue

                board.mark_cell(cur_marker, loc)
                self.n_explored_states += 1
                self.logger.debug('After marking board: \n{}'.format(board.board))

                # check whether if we have already seen this state
                is_max = cur_marker == marker
                key = StateCacheKey(board.board, is_max)
                has_key = self.cache and key in self.transposition_table
                equal_board = True
                if has_key:
                    self.logger.debug('Checking key: {}'.format(key))
                    value = self.transposition_table[key]
                    board_value_cache = value[0]
                    equal_board = np.allclose(board.board, board_value_cache, equal_nan=True)
                    if not equal_board:
                        shape0 = board.board.shape
                        shape1 = board_value_cache.shape
                        self.logger.debug('Hash key collision:')
                        self.logger.debug('Actual {}: \n{}'.format(shape0, board.board))
                        self.logger.debug('Cache {}: \n{}'.format(shape1, board_value_cache))
                        diff = board.board == board_value_cache
                        self.logger.debug('Locations that are equal: \n{}'.format(diff))

                if has_key and equal_board:
                    value = self.transposition_table[key]
                    utility = value[1] 
                    minimax_1 = [utility, utility]
                    empty_cells = []
                else:
                    minimax_1 = [-np.inf, np.inf]
                    empty_cells = board.get_empty_cells()

                # self.logger.info('Marking {!r} for player "{!r}"'.format(loc, cur_marker))
                next_marker = Marker.next_marker(cur_marker)
                # minimax_1 = [-np.inf] if is_max else [np.inf]
                # np.random.shuffle(empty_cells)
                node = (
                    depth + 1, loc, empty_cells, 
                    minimax_1, cur_marker, next_marker
                )
                node_stack.append(node)
            except Exception as e:
                self.logger.debug('Exception: {}'.format(e))
                self.logger.debug('No more children for {}'.format(last_loc))
                if board.state != BoardState.ONGOING:
                    # terminal state
                    utility = self.utility(board, marker, depth)
                else:
                    utility = minimax[1] if is_max else minimax[0]

                    # store the non-terminal state in transposition table
                    if self.cache and last_marker is not None:
                        is_max = last_marker == marker
                        key = StateCacheKey(board.board, is_max)
                        self.transposition_table[key] = (board.board, utility)

                node_stack.pop(-1)

                if node_stack:
                    # update parent's minimax
                    is_max = last_marker == marker
                    parent = node_stack[-1]
                    children_p = parent[2]
                    minimax_p = parent[3]
                    if is_max:
                        # parent[2][0] = max(parent[2][0], utility)
                        minimax_p[0] = max(minimax_p[0], utility)
                        if len(children_p) == 0:
                            minimax_p[1] = max(utility, minimax_p[0])
                    else:
                        minimax_p[1] = min(minimax_p[1], utility)
                        if len(children_p) == 0:
                            # we know it's a closed bound
                            minimax_p[0] = min(utility, minimax_p[1])
                        # parent[2][0] = min(parent[2][0], utility)
                    # self.logger.info('Unmarking {!r} for player "{!r}"'.format(last_loc, last_marker))
                    board.unmark_cell(last_marker, last_loc)
                else:
                    return utility

            # end = time.time()
            # took = (end - start) * 1000
            # print('Took: {:.3f}ms for a node'.format(took))
