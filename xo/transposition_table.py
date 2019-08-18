from xo import board_utils
import numpy as np
from collections import namedtuple


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

    def get_cache(self, state):
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
