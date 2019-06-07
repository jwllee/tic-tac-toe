from enum import Enum, IntEnum
from collections import namedtuple, Counter
from abc import ABC, abstractmethod, abstractclassmethod
import numpy as np
from . import utils


__all__ = [
    'Marker',
    'Cell',
    'BoardState', 
    'Board2d'
]


SEP = ','
Cell = namedtuple('Cell', ['content', 'loc'])


class Marker(IntEnum):
    def __str__(self):
        return str(self.name).capitalize()

    def __repr__(self):
        _map = {
            0: 'o',
            1: 'x'
        }
        return _map[self.value]

    CIRCLE = 0
    CROSS = 1


class BoardState(IntEnum):
    def __str__(self):
        return str(self.name).capitalize()

    ONGOING = 0
    DRAW = 1
    CIRCLE_WIN = 2
    CROSS_WIN = 3


class BoardType(Enum):
    def __str__(self):
        return str(self.name).capitalize()

    ORIGINAL = 0


class CellLocation(ABC):
    COORDINATE_FORMAT = ''

    def __init__(self, board_type):
        self.board_type = board_type
        self.coordinate = dict()

    #------------------------------------------------------------ 
    # Default implementations 
    #------------------------------------------------------------ 
    def __str__(self):
        return str(self.coordinate)
    
    #------------------------------------------------------------ 
    # Abstract methods
    #------------------------------------------------------------ 
    @abstractclassmethod
    def parse(self, s):
        raise NotImplementedError('Please implement this method.')


class Board(ABC):
    def __init__(self):
        self._state = BoardState.ONGOING
        self.observers = list()
        self.logger = utils.make_logger(Board.__name__)

    #------------------------------------------------------------ 
    # Observer pattern
    #------------------------------------------------------------ 
    def register_observer(self, obs):
        self.observers.append(obs)

    def remove_observer(self, obs):
        self.observers.remove(obs)

    def notify_observers(self):
        for obs in self.observers:
            obs.update(self)

    #------------------------------------------------------------ 
    # Properties
    #------------------------------------------------------------ 
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, s):
        raise NotImplementedError('Cannot set board state.')

    #------------------------------------------------------------ 
    # Abstract methods
    #------------------------------------------------------------ 
    @abstractmethod
    def restart(self):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def is_cell_empty(self, loc):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def get_cell(self, loc):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def get_empty_cells(self):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def get_filled_cells(self):
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
    class CellLocation(CellLocation):
        COORDINATE_FORMAT = 'r, c'
        ROW = 'row'
        COL = 'col'

        def __init__(self, row, col):
            super().__init__(BoardType.ORIGINAL)
            self.coordinate[self.ROW] = row
            self.coordinate[self.COL] = col

        @property
        def row(self):
            return self.coordinate[self.ROW]

        @property
        def col(self):
            return self.coordinate[self.COL]

        @classmethod
        def parse(self, s):
            row, col = s.split(SEP)
            return Board2d.CellLocation(int(row), int(col))

        def __str__(self):
            return '({}, {})'.format(self.row, self.col)

    def __init__(self, n_rows, n_cols):
        super().__init__()
        err_msg = 'Basic tic-tac-toe board has equal no. of rows and cols!'
        assert n_rows == n_cols, err_msg
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.board = np.full((self.n_rows, self.n_cols), np.nan)
        self.row_count = np.full((len(Marker), self.n_rows), 0)
        self.col_count = np.full((len(Marker), self.n_cols), 0)

    def restart(self):
        self.board = np.full((self.n_rows, self.n_cols), np.nan)
        self.row_count = np.full((len(Marker), self.n_rows), 0)
        self.col_count = np.full((len(Marker), self.n_cols), 0)
        self._state = BoardState.ONGOING

    #------------------------------------------------------------ 
    # Implementation of abstract methods
    #------------------------------------------------------------ 
    def is_cell_empty(self, loc):
        utils.assert_isinstance('cell location', self.CellLocation, loc)
        row, col = loc.row, loc.col
        if row < 0 or row > self.n_rows:
            raise ValueError('Row out of bounds [{}, {})'.format(0, self.n_rows))
        if col < 0 or col > self.n_cols:
            raise ValueError('Column out of bounds [{}, {})'.format(0, self.n_cols))
        return np.isnan(self.board[row, col])

    def get_cell(self, loc):
        utils.assert_isinstance('cell location', self.CellLocation, loc)
        row, col = loc.row, loc.col
        cell_v = self.board[row, col]
        marker = None if cell_v == np.nan else Marker(cell_v + Marker.CIRCLE)
        return Cell(marker, loc)

    def get_empty_cells(self):
        locs = np.argwhere(np.isnan(self.board))
        cells = list()
        self.logger.debug('Empty cell locs: {}'.format(locs))
        for row, col in locs:
            loc = self.CellLocation(row, col)
            cell = Cell(np.nan, loc)
            cells.append(cell)
        return cells

    def get_filled_cells(self):
        locs = np.where(self.board != np.nan) 
        locs = np.argwhere(~np.isnan(self.board))
        cells = list()
        for row, col in locs:
            loc = self.CellLocation(row, col)
            val = Marker.CIRCLE + self.board[row, col]
            cell = Cell(val, loc)
            cells.append(cell)
        return cells

    @property
    def full(self):
        return not np.isnan(self.board).any()

    def mark_cell(self, marker, loc):
        self.logger.debug('Marking "{!r}" at {}'.format(marker, loc))
        utils.assert_isinstance('marker', Marker, marker)
        err_msg = 'Game state is not ongoing: {}'.format(self.state)
        assert self.state == BoardState.ONGOING, err_msg

        utils.assert_isinstance('cell location', self.CellLocation, loc)
        row, col = loc.row, loc.col
        
        # check if it's already marked
        if not np.isnan(self.board[row, col]):
            return False
        else:
            self.board[row, col] = marker
            # update row, column, and diagonal count
            self.row_count[marker, row] += 1
            self.col_count[marker, col] += 1
            self.logger.debug('row count: \n{}'.format(self.row_count))
            self.logger.debug('col count: \n{}'.format(self.col_count))
            self.__update_state(row, col)
            # update observers
            self.notify_observers()
            return True
    #------------------------------------------------------------ 

    def get_diag_count(self, start_ind, left2right=True):
        if left2right:
            diag = np.diag(self.board, start_ind)
        else:
            diag = np.diag(np.fliplr(self.board), start_ind)

        diag_dict = dict()
        for marker in Marker:
            filtered = filter(lambda a: a == marker, diag)
            diag_dict[marker] = len(list(filtered))

        return diag_dict

    def __update_state(self, row, col):
        self.logger.debug('Updating board state')
        # 1. check row 
        winner = np.where(self.row_count[:, row] == self.n_rows)[0]
        self.logger.debug('Winner at row {}: {}'.format(row, winner))
        if winner.shape[0] > 0:
            marker = Marker(winner[0])
            self._state = BoardState(BoardState.CIRCLE_WIN.value + winner[0])
            msg = '"{!r}" win at row {}'
            msg = msg.format(marker, row)
            self.logger.debug(msg)
            return

        # 2. check col
        winner = np.where(self.col_count[:, col] == self.n_cols)[0]
        if winner.shape[0] > 0:
            marker = Marker(winner[0])
            self._state = BoardState(BoardState.CIRCLE_WIN.value + winner[0])
            msg = '"{!r}" win at col {}'
            msg = msg.format(marker, col)
            self.logger.debug(msg)
            return 

        # 3. check diagonals
        if row == col: # left to right diagonal
            diag_count = self.get_diag_count(0)
            
            for marker in Marker:
                if diag_count[marker] == self.n_rows:
                    self._state = BoardState(BoardState.CIRCLE_WIN + marker)
                    msg = '"{!r}" win at diagonal'.format(marker)
                    self.logger.debug(msg)
                    return

        elif row + col == self.n_rows - 1: # right to left diagonal
            diag_count = self.get_diag_count(self.n_rows - 1)

            for marker in Marker:
                if diag_count[marker] == self.n_rows:
                    self._state = BoardState(BoardState.CIRCLE_WIN + marker)
                    msg = '"{!r}" win at diagonal'.format(marker)
                    self.logger.debug(msg)
                    return

        # 4. check if there is any more empty cells
        if self.full:
            self._state = BoardState.DRAW
