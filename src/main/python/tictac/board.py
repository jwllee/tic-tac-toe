from enum import Enum
from collections import namedtuple, Counter
from abc import ABC, abstractmethod
import numpy as np
from . import utils


__all__ = [
    'Marker',
    'Cell',
    'BoardState', 
    'Board2d'
]


SEP = ','
Cell = namedtuple('Cell', ['row', 'col', 'val'])


class Marker(Enum):
    def __str__(self):
        return str(self.name).capitalize()

    @property
    def marker(self):
        _map = {
            0: 'o',
            1: 'x'
        }
        return _map[self.value]

    CIRCLE = 0
    CROSS = 1


class BoardState(Enum):
    ONGOING = 0
    DRAW = 1
    CIRCLE_WIN = 2
    CROSS_WIN = 3


class Board(ABC):
    EMPTY = -1

    def __init__(self):
        self.__state = BoardState.ONGOING
        self.__coordinate_format = None
        self.observers = list()

    #------------------------------------------------------------ 
    # Observer pattern
    #------------------------------------------------------------ 
    def register_observer(obs):
        self.observers.append(obs)

    def remove_observer(obs):
        self.observers.remove(obs)

    def notify_observers():
        for obs in self.observers:
            obs.update(self)

    #------------------------------------------------------------ 
    # Properties
    #------------------------------------------------------------ 
    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, s):
        raise NotImplementedError('Cannot set board state.')

    @property
    def coordinate_format(self):
        return self.__coordinate_format

    @coordinate_format.setter
    def coordinate_format(self, _format):
        raise NotImplementedError('Cannot set board coordinate format!')

    #------------------------------------------------------------ 
    # Abstract methods
    #------------------------------------------------------------ 
    @abstractmethod
    def restart(self):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def is_cell_empty(self, row, col):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def get_cell(self, row, col):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def is_move_valid(self, move):
        raise NotImplementedError('Please implement this method.')

    @property
    def full(self):
        raise NotImplementedError('Please implement this method.')

    @full.setter
    def full(self, v):
        raise NotImplementedError('Cannot set board full property!')

    @abstractmethod
    def mark_cell(self, marker, loc):
        raise NotImplementedError('Please implement this method.') 


class Board2d(Board):
    def __init__(self, n_rows, n_cols):
        super().__init__(self)
        err_msg = 'Basic tic-tac-toe board has equal no. of rows and cols!'
        assert n_rows == n_cols, err_msg
        self.__coordinate_format = 'r,c'
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.board = np.full((self.n_rows, self.n_cols), Board.EMPTY)
        self.row_count = np.full((len(Marker), self.n_rows), 0)
        self.col_count = np.full((len(Marker), self.n_cols), 0)

    def restart(self):
        self.board = np.full((self.n_rows, self.n_cols), Board.EMPTY)
        self.row_count = np.full((len(Marker), self.n_rows), 0)
        self.col_count = np.full((len(Marker), self.n_cols), 0)

    #------------------------------------------------------------ 
    # Implementation of abstract methods
    #------------------------------------------------------------ 
    def is_cell_empty(self, row, col):
        if row < 0 or row > self.n_rows:
            raise ValueError('Row out of bounds [{}, {})'.format(0, self.n_rows))
        if col < 0 or col > self.n_cols:
            raise ValueError('Column out of bounds [{}, {})'.format(0, self.n_cols))
        return self.board[row, col] == Board.EMPTY

    def get_cell(self, row, col):
        cell_v = self.board[row, col]
        marker = None if cell_v == Board.EMPTY else cell_v
        return Cell(row, col, marker)

    def is_move_valid(self, move):
        row, col = move.split(SEP)
        return self.board[row, col] == Board.EMPTY

    @property
    def full(self):
        return (self.board == Board.EMPTY).any()

    def mark_cell(self, marker, loc):
        utils.assert_isinstance('marker', Marker, marker)
        err_msg = 'Game state is not ongoing: {}'.format(self.__current_state)
        assert self.__current_state == BoardState.ONGOING, err_msg
        
        row, col = loc
        # check if it's already marked
        if self.board[row, col] != Board.EMPTY:
            return False
        else:
            self.board[row, col] = marker
            # update row, column, and diagonal count
            self.row_count[marker, row] += 1
            self.col_count[marker, col] += 1
            # update observers
            self.notify_observers()
            return True
    #------------------------------------------------------------ 

    def get_row_count(self, row):
        if row < 0 or row > self.n_rows:
            raise ValueError('Row out of bounds [{}, {})'.format(0, self.n_rows))
        row_dict = dict()
        for marker in Marker:
            row_dict[marker] = self.row_count[marker, row]

        return row_dict

    def get_col_count(self, col):
        if col < 0 or col > self.n_cols:
            raise ValueError('Column out of bounds [{}, {})'.format(0, self.n_cols))

        col_dict = dict()
        for marker in Marker:
            col_dict[marker] = self.col_count[marker, col]

        return col_dict

    def get_diag_count(self, start_ind, left2right=True):
        if left2right:
            diag = np.diag(mat, start_ind)
        else:
            diag = np.diag(np.fliplr(mat), start_ind)

        diag_dict = dict()
        for marker in Marker:
            filtered = filter(lambda a: a == marker, diag)
            diag_dict[marker] = len(list(filtered))

        return diag_dict

    def __update_state(self, row, col):
        # 1. check row 
        row_count = self.get_row_count(row)
        for marker in Marker:
            if row_count[marker] == self.n_rows:
                self.__current_state = BoardState.CIRCLE_WIN + marker
                return

        # 2. check col
        col_count = self.get_col_count(col)
        for marker in Marker:
            if col_count[marker] == self.n_cols:
                self.__current_state = BoardState.CIRCLE_WIN + marker
                return

        # 3. check diagonals
        if row == col: # left to right diagonal
            diag_count = self.get_diag_count(0)
            
            for marker in Marker:
                if diag_count[marker] == self.n_rows:
                    self.__current_state = BoardState.CIRCLE_WIN + marker
                    return

        elif row + col == n_rows - 1: # right to left diagonal
            diag_count = self.get_diag_count(n_rows - 1)

            for marker in Marker:
                if diag_count[marker] == self.n_rows:
                    self.__current_state = BoardState.CIRCLE_WIN + marker
                    return

        # 4. check if there is any more empty cells
        if self.full():
            self.__current_state = BoardState.DRAW
