from .. import board_utils
from ..utils import make_logger
import numpy as np
from collections import namedtuple


logger = make_logger('transposition_table.py')


field_names = [
    'board_x',
    'board_o',
    'n_rows',
    'n_cols',
    'n_connects',
    'depth',
    'flag',
    'value'
]
Cache = namedtuple('Cache', field_names)


field_names = [
    'n_rows',
    'n_cols',
    'n_connects',
    'board_x',
    'board_o',
]
State = namedtuple('State', field_names)


def addition_hash(arr, sz):
    # taken from: https://stackoverflow.com/questions/19854564/hash-integer-array
    hash_ = 17
    for i in range(sz):
        v = arr[i]
        hash_ = (hash_ * 19) + ord(v)
    return hash_


def hash_state(state):
    n_cells = state.n_rows * state.n_cols
    board_x = state.board_x
    board_o = state.board_o

    board_str = board_utils.get_board_str(board_x, board_o, n_cells)
    hash_ = addition_hash(board_str, n_cells)
    return hash_


class TTable:
    def __init__(self):
        self.table = dict()

    def __get_cache(self, state):
        hash_ = hash_state(state)
        res = None
        if hash_ in self.table:
            res = self.table[hash_]
            # check if it is in fact the state
            same_board_x = res.board_x == state.board_x
            same_board_o = res.board_o == state.board_o
            if not same_board_x or not same_board_o:
                res = None
        return res

    def get_cache(self, state):
        res = self.__get_cache(state)
        board_x = state.board_x
        board_o = state.board_o
        n_rows = state.n_rows
        n_cols = state.n_cols
        n_connects = state.n_connects
        if not res:
            # try reflecting the board on x axis
            board_x_r = board_utils.reflect_x(board_x, n_rows, n_cols)
            board_o_r = board_utils.reflect_x(board_o, n_rows, n_cols)
            reflected = State(n_rows, n_cols, n_connects, board_x_r, board_o_r)
            res = self.__get_cache(reflected)
            # if not None, change it back to original board
            if res:
                # info_msg = 'Found cache via reflection on x axis'
                # logger.info(info_msg)
                res = Cache(board_x, board_o, n_rows, n_cols, n_connects, res.depth, res.flag, res.value)

        if not res:
            # try reflecting the board on y axis
            board_x_r = board_utils.reflect_y(board_x, n_rows, n_cols)
            board_o_r = board_utils.reflect_y(board_o, n_rows, n_cols)
            reflected = State(n_rows, n_cols, n_connects, board_x_r, board_o_r)
            res = self.__get_cache(reflected)
            # if not None, change it back to original board
            if res:
                # info_msg = 'Found cache via reflection on y axis'
                # logger.info(info_msg)
                res = Cache(board_x, board_o, n_rows, n_cols, n_connects, res.depth, res.flag, res.value)

        return res

    def save_cache(self, state, depth, utility, flag):
        cache = Cache(
            state.board_x,
            state.board_o,
            state.n_rows,
            state.n_cols,
            state.n_connects,
            depth, flag, utility
        )
        hash_ = hash_state(state)
        self.table[hash_] = cache
