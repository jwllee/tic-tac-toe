from abc import ABC, abstractclassmethod
from enum import IntEnum
from collections import namedtuple


from xo import utils


__all__ = [
    'SEP',
    'Cell',
    'Marker',
    'BoardState',
    'AbstractCellLocation'
]


SEP = ','
Cell = namedtuple('Cell', ['val', 'loc'])


class Marker(IntEnum):
    def __str__(self):
        return str(self.name).capitalize()

    def __repr__(self):
        _map = {
            0: 'o',
            1: 'x'
        }
        return _map[self.value]

    @classmethod
    def next_marker(cls, marker):
        return Marker((marker + 1) % len(Marker))

    CIRCLE = 0
    CROSS = 1


class BoardState(IntEnum):
    def __str__(self):
        return str(self.name).capitalize()

    ONGOING = 0
    DRAW = 1
    CIRCLE_WIN = 2
    CROSS_WIN = 3


class AbstractCellLocation(ABC):
    def __init__(self, board_type):
        self.board_type = board_type
    
    #------------------------------------------------------------ 
    # Abstract methods
    #------------------------------------------------------------ 
    @abstractclassmethod
    def parse(self, s):
        raise NotImplementedError('Please implement this method.')


def is_winner_state(state):
    return state - BoardState.CIRCLE_WIN >= 0


def assert_cell_location(l0, l1):
    utils.assert_isinstance('Cell location', AbstractCellLocation, loc)
    # check board type
    bd_type_err = 'Mismatch in board type\n'
    bd_type_err += '[left]: {left}\n'
    bd_type_err += '[right]: {right}\n'
    bd_type_err = bd_type_err.format(left=l0.board_type,
                                     right=l1.board_type)
    assert l0.board_type == l1.board_type, bd_type_err
