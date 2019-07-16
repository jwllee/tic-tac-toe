import numpy as np

from xo import utils
from xo.board.base import *
from xo.board.utils import *
from xo.board import utils as bd_utils


__all__ = [
    'CellLocation2d',
    'Board2d'
]


class CellLocation2d(AbstractCellLocation):
    COORDINATE_FORMAT = 'r,c'

    def __init__(self, row, col):
        super().__init__(type(Board2d))
        self._row = row
        self._col = col

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @classmethod
    def parse(self, s):
        s = s.replace('(', '').replace(')', '')
        row, col = s.split(SEP)
        return CellLocation2d(int(row), int(col))

    def __repr__(self):
        return '({}, {})'.format(self.row, self.col)

    def __str__(self):
        return str(repr(self))

    def __eq__(self, other):
        bd_utils.assert_cell_location(self, other)
        return self.row == other.row and self.col == other.col

    def __neq__(self, other):
        return not self == other

    def __hash__(self):
        return hash((0, self.row)) + hash((1, self.col))


class Board2d(AbstractBoard):
    MIN_DIM = 3
    MAX_DIM = 5
    MIN_CONNECT = 3

    def __init__(self, n_rows, n_cols, n_connects):
        super().__init__()
        # Check that 
        # - MIN_DIM <= n_rows <= MAX_DIM
        # - MIN_DIM <= n_cols <= MAX_DIM
        dim_err = '{} dimension {} not in [{}, {}]'
        dim_err_row = dim_err.format('Row', n_rows, 
                                     self.MIN_DIM, self.MAX_DIM)
        dim_err_col = dim_err.format('Col', n_rows, 
                                     self.MIN_DIM, self.MAX_DIM)
        row_assert = n_rows >= self.MIN_DIM and n_rows <= self.MAX_DIM
        col_assert = n_cols >= self.MIN_DIM and n_cols <= self.MAX_DIM
        if not row_assert:
            raise ValueError(dim_err_row)
        if not col_assert:
            raise ValueError(dim_err_col)

        # Check that MIN_CONNECT <= n_connect <= min(n_rows, n_cols)
        connect_min_assert = n_connects >= self.MIN_CONNECT
        connect_max = min(n_rows, n_cols)
        connect_max_assert = n_connects <= connect_max
        connect_err = '{} connect to win not in [{}, {}]'
        connect_err = connect_err.format(n_connects,
                                         self.MIN_CONNECT,
                                         connect_max)
        if not connect_min_assert or not connect_max_assert:
            raise ValueError(connect_err)

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_connects = n_connects
        self.board = np.full((self.n_rows, self.n_cols), np.nan)
        self.row_count = self.make_row_count(n_rows, n_cols, n_connects)
        self.col_count = self.make_col_count(n_rows, n_cols, n_connects)
        self.l2r_diag_count = self.make_diag_count(n_rows, n_cols, n_connects)
        self.r2l_diag_count = self.make_diag_count(n_rows, n_cols, n_connects)

    def make_row_count(self, n_rows, n_cols, n_connects):
        n_levels = n_cols - n_connects + 1
        n_markers = len(Marker)
        return np.full((n_markers, n_rows, n_levels), 0)

    def make_col_count(self, n_rows, n_cols, n_connects):
        n_levels = n_rows - n_connects + 1
        n_markers = len(Marker)
        return np.full((n_markers, n_cols, n_levels), 0)

    def make_diag_count(self, n_rows, n_cols, n_connects):
        n_markers = len(Marker)
        n_diags = n_cols - n_connects + 1
        n_levels = n_rows - n_connects + 1
        return np.full((n_markers, n_diags, n_levels), 0)

    #------------------------------------------------------------ 
    # Properties
    #------------------------------------------------------------ 
    @property
    def n_cells(self):
        return self.board.size

    @property
    def has_winner(self):
        return bd_utils.is_winner_state(self.state)

    #------------------------------------------------------------ 
    # Abstract methods
    #------------------------------------------------------------ 
    def copy(self, register_observers=False):
        copied = Board2d(self.n_rows, self.n_cols)
        copied._state = self._state
        copied.board = self.board.copy()
        copied.row_count = self.row_count.copy()
        copied.col_count = self.col_count.copy()

        if register_observers:
            for obs in self.observers:
                copied.register_observer(obs)

        return copied

    def __hash__(self):
        return hash(self.board.data.tobytes())

    def restart(self):
        self.board = np.full((self.n_rows, self.n_cols), np.nan)
        self.row_count = self.make_row_count(self.n_rows, 
                                             self.n_cols, 
                                             self.n_connects)
        self.col_count = self.make_col_count(self.n_rows,
                                             self.n_cols,
                                             self.n_connects)
        self.l2r_diag_count = self.make_diag_count(self.n_rows,
                                                   self.n_cols,
                                                   self.n_connects)
        self.r2l_diag_count = self.make_diag_count(self.n_rows,
                                                   self.n_cols,
                                                   self.n_connects)
        self._state = BoardState.ONGOING

    def is_cell_empty(self, loc):
        utils.assert_isinstance('Cell location', CellLocation2d, loc)
        row, col = loc.row, loc.col

        bound_err = '{} out of bounds [{}, {})'
        if row < 0 or row > self.n_rows:
            bound_err_row = bound_err.format('Row', 0, self.n_rows)
            raise ValueError(bound_err_row)

        if col < 0 or col > self.n_cols:
            bound_err_col = bound_err.format('Col', 0, self.n_cols)
            raise ValueError(bound_err_col)

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
            loc = CellLocation2d(row, col)
            cell = Cell(np.nan, loc)
            cells.append(cell)
        return cells

    def get_filled_cells(self):
        locs = np.argwhere(~np.isnan(self.board))
        cells = list()
        for row, col in locs:
            loc = CellLocation2d(row, col)
            val = Marker.CIRCLE + self.board[row, col]
            cell = Cell(val, loc)
            cells.append(cell)
        return cells

    @property
    def full(self):
        return not np.isnan(self.board).any()

    @property
    def empty(self):
        return np.isnan(self.board).all()

    def mark_cell(self, marker, loc):
        self.logger.debug('Marking "{!r}" at {}'.format(marker, loc))
        utils.assert_isinstance('marker', Marker, marker)
        err_msg = 'Game state is not ongoing: {}'.format(self.state)
        assert self.state == BoardState.ONGOING, err_msg

        utils.assert_isinstance('cell location', CellLocation2d, loc)
        row, col = loc.row, loc.col
        
        # check if it's already marked
        if not np.isnan(self.board[row, col]):
            return False
        else:
            self.board[row, col] = int(marker)
            # update row, column, and diagonal count
            self.update_row_count(marker, row, col)
            self.update_col_count(marker, row, col)
            self.update_l2r_diag_count(marker, row, col)
            self.update_r2l_diag_count(marker, row, col)
            self.update_state(row, col)
            # update observers
            cell = Cell(int(marker), loc)
            data = { NotificationKey.CELL: cell }
            self.notify_observers(NotificationType.CELL, data)
            return True

    def unmark_cell(self, marker, loc):
        utils.assert_isinstance('marker', Marker, marker)
        utils.assert_isinstance('cell location', CellLocation2d, loc)

        row, col = loc.row, loc.col
        # check if that cell is in fact marked
        if np.isnan(self.board[row, col]):
            raise ValueError('Cell at {} is not marked.'.format(loc))

        self.board[row, col] = np.nan
        self.update_row_count(None, row, col)
        self.update_col_count(None, row, col)
        self.update_l2r_diag_count(None, row, col)
        self.update_r2l_diag_count(None, row, col)
        self._state = BoardState.ONGOING
        self.eval_state()
        # update observers
        cell = Cell(np.nan, loc)
        data = { NotificationKey.CELL: cell }
        self.notify_observers(NotificationType.CELL, data)

    def is_winner(self, marker):
        winner_int = self.state - BoardState.CIRCLE_WIN
        return self.has_winner and Marker(winner_int) == marker

    #------------------------------------------------------------ 
    # Board2d methods
    #------------------------------------------------------------ 
    def update_row_count(self, marker, row, col):
        # suppose that col is the last cell of the row to get the lowest
        # possible level no.
        start_level = max(0, col - self.n_connects + 1)
        n_levels = self.row_count.shape[2]
        # suppose that col is the first cell of last possible level
        end_level = min(col + 1, n_levels)
        # have to include level 0 at least
        end_level = 1 if end_level <= 0 else end_level

        # debugging
        debug_msg = 'Row update ({}, {}) between [{}, {})'
        debug_msg = debug_msg.format(row, col, start_level, end_level)
        self.logger.debug(debug_msg)

        for level in range(start_level, end_level):
            if marker is None:
                self.row_count[marker, row, level] -= 1
            else:
                self.row_count[marker, row, level] += 1

    def update_col_count(self, marker, row, col):
        start_level = max(0, row - self.n_connects + 1)
        n_levels = self.col_count.shape[2]
        end_level = min(row + 1, n_levels)
        end_level = 1 if end_level <= 0 else end_level

        # debugging
        debug_msg = 'Row update ({}, {}) between [{}, {})'
        debug_msg = debug_msg.format(row, col, start_level, end_level)
        self.logger.debug(debug_msg)

        for level in range(start_level, end_level):
            if marker is None:
                self.col_count[marker, col, level] -= 1
            else:
                self.col_count[marker, col, level] += 1

    def get_diag_ids(self, row, col, left2right=True):
        res = dict()

        n_levels = self.l2r_diag_count.shape[2]
        max_diag_id = self.l2r_diag_count.shape[1]

        for level in range(0, n_levels):
            level_diff = level - row

            if left2right:
                diag_id = col + level_diff
            else:
                diag_id = col - level_diff - self.n_connects + 1

            if diag_id >= 0 and diag_id < max_diag_id:
                res[level] = diag_id

        return res

    def update_l2r_diag_count(self, marker, row, col):
        n_levels = self.l2r_diag_count.shape[2]
        max_diag_id = self.l2r_diag_count.shape[1]

        for level, diag_id in self.get_diag_ids(row, col).items():
            if marker is None:
                self.l2r_diag_count[marker, diag_id, level] -= 1
            else:
                self.l2r_diag_count[marker, diag_id, level] += 1

    def update_r2l_diag_count(self, marker, row, col):
        n_levels = self.r2l_diag_count.shape[2]
        max_diag_id = self.r2l_diag_count.shape[1]

        for level, diag_id in self.get_diag_ids(row, col, False).items():
            if marker is None:
                self.r2l_diag_count[marker, diag_id, level] -= 1
            else:
                self.r2l_diag_count[marker, diag_id, level] += 1

    def row_has_winner(self, row):
        has_winner = False
        n_levels = self.row_count.shape[2]
        for l in range(0, n_levels):
            winner = np.where(self.row_count[:, row, l] == self.n_connects)[0]
            debug_msg = 'Winner at row {} level {}: {}'
            debug_msg = debug_msg.format(row, l, winner)
            self.logger.debug(debug_msg)

            if winner.shape[0] > 0:
                marker = Marker(winner[0])
                state_val = BoardState.CIRCLE_WIN.value + winner[0]
                self._state = BoardState(state_val)
                msg = '"{!r}" win at row {}'
                msg = msg.format(marker, row)
                self.logger.debug(msg)
                has_winner = True
                break
                
        return has_winner

    def col_has_winner(self, col):
        has_winner = False
        n_levels = self.col_count.shape[2]
        for l in range(0, n_levels):
            winner = np.where(self.col_count[:, col, l] == self.n_connects)[0]

            debug_msg = 'Winner at col {} level {}: {}'
            debug_msg = debug_msg.format(col, l, winner)
            self.logger.debug(debug_msg)

            if winner.shape[0] > 0:
                marker = Marker(winner[0])
                state_val = BoardState.CIRCLE_WIN.value + winner[0]
                self._state = BoardState(state_val)
                msg = '"{!r}" win at col {}'
                msg = msg.format(marker, col)
                self.logger.debug(msg)
                has_winner = True
                break

        return has_winner

    def diag_has_winner(self, diag_id, level, left2right=True):
        cond = diag_count[:, diag_id, level] == self.n_connects
        winner = np.where(cond)[0]

        debug_msg = 'Winner at diag {} level {}: {}'
        debug_msg = debug_msg.format(diag_id, level, winner)
        self.logger.debug(debug_msg)

        if winner.shape[0] > 0:
            marker = Marker(winner[0])
            state_val = BoardState.CIRCLE_WIN.value + winner[0]
            self._state = BoardState(state_val)
            msg = '"{!r}" win at diag {}'
            msg = msg.format(marker, diag_id)
            self.logger.debug(msg)
            has_winner = True

        return has_winner

    def eval_state(self):
        # check rows
        for row in range(self.n_rows):
            if self.row_has_winner(row):
                data = { NotificationKey.STATE: self.state }
                self.notify_observers(NotificationType.STATE, data)
                return

        # check cols
        for col in range(self.n_cols):
            if self.col_has_winner(col):
                data = { NotificationKey.STATE: self.state }
                self.notify_observers(NotificationType.STATE, data)
                return

        # check diagonals
        n_diags = self.l2r_diag_count.shape[1]
        n_levels = self.l2r_diag_count.shape[2]
        for level in range(n_levels):
            for diag_id in range(n_diags):
                if self.diag_has_winner(diag_id, level, left2right=True):
                    data = { NotificationKey.STATE: self.state }
                    self.notify_observers(NotificationType.STATE, data)
                    return
                if self.diag_has_winner(diag_id, level, left2right=False):
                    data = { NotificationKey.STATE: self.state }
                    self.notify_observers(NotificationType.STATE, data)
                    return

        if self.full:
            self._state = BoardState.DRAW
            data = { NotificationKey.STATE: self.state }
            self.notify_observers(NotificationType.STATE, data)

    def update_state(self, row, col):
        # 1. check row 
        if self.row_has_winner(row):
            data = { NotificationKey.STATE: self.state }
            self.notify_observers(NotificationType.STATE, data)
            return

        # 2. check col
        if self.col_has_winner(col):
            data = { NotificationKey.STATE: self.state }
            self.notify_observers(NotificationType.STATE, data)
            return

        # 3. check diagonals
        # left to right diagonal
        for level, diag_id in self.get_diag_ids(row, col).items():
            if self.diag_has_winner(diag_id, level, left2right=True):
                data = { NotificationKey.STATE: self.state }
                self.notify_observers(NotificationType.STATE, data)
                return

        # right to left diagonal
        for level, diag_id in self.get_diag_ids(row, col, False).items():
            if self.diag_has_winner(diag_id, level, left2right=False):
                data = { NotificationKey.STATE: self.state }
                self.notify_observers(NotificationType.STATE, data)
                return

        # 4. check if there is any more empty cells
        if self.full:
            self._state = BoardState.DRAW
            data = { NotificationKey.STATE: self.state }
            self.notify_observers(NotificationType.STATE, data)
