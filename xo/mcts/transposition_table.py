from .. import board_utils
from ..utils import make_logger
from collections import namedtuple
import numpy as np


logger = make_logger('mcts.transposition_table.py')




def addition_hash(arr, sz):
    # taken from: https://stackoverflow.com/questions/19854564/hash-integer-array
    hash_ = 17
    for i in range(sz):
        v = arr[i]
        hash_ = (hash_ * 19) + ord(v)
    return hash_


def hash_node(node, n_cells):
    board_str = board_utils.get_board_str(node.board_x, node.board_o, n_cells)
    hash_ = addition_hash(board_str, n_cells)
    return hash_


