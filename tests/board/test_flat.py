import pytest


from xo.board import *
from xo.board.utils import *
from xo.utils import *


class TestCellLocation2d:
    def test_init_loc(self):
        row, col = 0, 0
        cell_loc = CellLocation2d(row, col)
        assert_isinstance('CellLocation2d', CellLocation2d, cell_loc)


class TestBoard2d:
    def test_init_board(self):
        n_rows, n_cols, n_connects = 3, 3, 3
        board = Board2d(n_rows, n_cols, n_connects)
        assert_isinstance('Board2d', Board2d, board)

    def test_3x3x3_row_count_shape(self):
        n_rows, n_cols, n_connects = 3, 3, 3
        board = Board2d(n_rows, n_cols, n_connects)
        row_count = board.make_row_count(n_rows, n_cols, n_connects)
        expected = (2, 3, 1)
        assert row_count.shape == expected

    def test_3x4x3_row_count_shape(self):
        n_rows, n_cols, n_connects = 3, 4, 3
        board = Board2d(n_rows, n_cols, n_connects)
        row_count = board.make_row_count(n_rows, n_cols, n_connects)
        expected = (2, 3, 2)
        assert row_count.shape == expected

    def test_4x4x4_row_count_shape(self):
        n_rows, n_cols, n_connects = 4, 4, 4
        board = Board2d(n_rows, n_cols, n_connects)
        row_count = board.make_row_count(n_rows, n_cols, n_connects)
        expected = (2, 4, 1)
        assert row_count.shape == expected

    def test_5x3x3_row_count_shape(self):
        n_rows, n_cols, n_connects = 5, 3, 3
        board = Board2d(n_rows, n_cols, n_connects)
        row_count = board.make_row_count(n_rows, n_cols, n_connects)
        expected = (2, 5, 1)

    def test_3x3x3_col_count_shape(self):
        n_rows, n_cols, n_connects = 3, 3, 3
        board = Board2d(n_rows, n_cols, n_connects)
        col_count = board.make_col_count(n_rows, n_cols, n_connects)
        expected = (2, 3, 1)
        assert col_count.shape == expected

    def test_3x4x3_col_count_shape(self):
        n_rows, n_cols, n_connects = 3, 4, 3
        board = Board2d(n_rows, n_cols, n_connects)
        col_count = board.make_col_count(n_rows, n_cols, n_connects)
        expected = (2, 4, 1)
        assert col_count.shape == expected

    def test_4x4x4_col_count_shape(self):
        n_rows, n_cols, n_connects = 4, 4, 4
        board = Board2d(n_rows, n_cols, n_connects)
        col_count = board.make_col_count(n_rows, n_cols, n_connects)
        expected = (2, 4, 1)
        assert col_count.shape == expected

    def test_3x3x3_diag_count_shape(self):
        n_rows, n_cols, n_connects = 3, 3, 3
        board = Board2d(n_rows, n_cols, n_connects)
        diag_count = board.make_diag_count(n_rows, n_cols, n_connects)
        expected = (2, 1, 1)
        assert diag_count.shape == expected

    def test_3x4x3_diag_count_shape(self):
        n_rows, n_cols, n_connects = 3, 4, 3
        board = Board2d(n_rows, n_cols, n_connects)
        diag_count = board.make_diag_count(n_rows, n_cols, n_connects)
        expected = (2, 2, 1)
        assert diag_count.shape == expected

    def test_4x4x3_diag_count_shape(self):
        n_rows, n_cols, n_connects = 4, 4, 3
        board = Board2d(n_rows, n_cols, n_connects)
        diag_count = board.make_diag_count(n_rows, n_cols, n_connects)
        expected = (2, 2, 2)
        assert diag_count.shape == expected

    def test_4x5x3_diag_count_shape(self):
        n_rows, n_cols, n_connects = 4, 5, 3
        board = Board2d(n_rows, n_cols, n_connects)
        diag_count = board.make_diag_count(n_rows, n_cols, n_connects)
        expected = (2, 3, 2)
        assert diag_count.shape == expected

    def test_4x4x4_diag_count_shape(self):
        n_rows, n_cols, n_connects = 4, 4, 4
        board = Board2d(n_rows, n_cols, n_connects)
        diag_count = board.make_diag_count(n_rows, n_cols, n_connects)
        expected = (2, 1, 1)
        assert diag_count.shape == expected

    def test_3x3x3_update_row_count(self):
        n_rows, n_cols, n_connects = 3, 3, 3
        board = Board2d(n_rows, n_cols, n_connects)
        # update (1, 1)
        row, col, marker = 1, 1, Marker.CIRCLE
        assert board.row_count[marker, row, 0] == 0
        board.update_row_count(marker, row, col)
        assert board.row_count[marker, row, 0] == 1
        # update (0, 0)
        row, col, marker = 0, 0, Marker.CROSS
        assert board.row_count[marker, row, 0] == 0
        board.update_row_count(marker, row, col)
        assert board.row_count[marker, row, 0] == 1
        # update (2, 2)
        row, col, marker = 0, 0, Marker.CIRCLE
        assert board.row_count[marker, row, 0] == 0
        board.update_row_count(marker, row, col)
        assert board.row_count[marker, row, 0] == 1

    def test_3x4x3_update_row_count(self):
        n_rows, n_cols, n_connects = 3, 4, 3
        board = Board2d(n_rows, n_cols, n_connects)
        # update (0, 0)
        row, col, marker = 0, 0, Marker.CIRCLE
        assert board.row_count.sum(axis=None) == 0 
        board.update_row_count(marker, row, col)
        assert board.row_count[marker, row, 0] == 1
        # update (1, 1)
        board.restart()
        row, col, marker = 1, 1, Marker.CROSS
        assert board.row_count.sum(axis=None) == 0 
        board.update_row_count(marker, row, col)
        assert board.row_count[marker, row, 0] == 1
        assert board.row_count[marker, row, 1] == 1
        # update (2, 2)
        board.restart()
        row, col, marker = 2, 2, Marker.CIRCLE
        assert board.row_count.sum(axis=None) == 0 
        board.update_row_count(marker, row, col)
        assert board.row_count[marker, row, 0] == 1
        assert board.row_count[marker, row, 1] == 1
        # update (2, 3)
        board.restart()
        row, col, marker = 2, 3, Marker.CROSS
        assert board.row_count.sum(axis=None) == 0 
        board.update_row_count(marker, row, col)
        assert board.row_count[marker, row, 0] == 0
        assert board.row_count[marker, row, 1] == 1

    def test_3x3x3_update_col_count(self):
        n_rows, n_cols, n_connects = 3, 3, 3
        board = Board2d(n_rows, n_cols, n_connects)
        # update (0, 0)
        row, col, marker = 0, 0, Marker.CIRCLE
        assert board.col_count[marker, col, 0] == 0
        board.update_col_count(marker, row, col)
        assert board.col_count[marker, col, 0] == 1
        # update (1, 1)
        row, col, marker = 1, 1, Marker.CROSS
        assert board.col_count[marker, col, 0] == 0
        board.update_col_count(marker, row, col)
        assert board.col_count[marker, col, 0] == 1
        # update (2, 2)
        row, col, marker = 2, 2, Marker.CIRCLE
        assert board.col_count[marker, col, 0] == 0
        board.update_col_count(marker, row, col) 
        assert board.col_count[marker, col, 0] == 1
        # update (0, 2)
        row, col, marker = 0, 2, Marker.CROSS
        assert board.col_count[marker, col, 0] == 0
        board.update_col_count(marker, row, col)
        assert board.col_count[marker, col, 0] == 1

    def test_4x3x3_update_col_count(self):
        n_rows, n_cols, n_connects = 4, 3, 3
        board = Board2d(n_rows, n_cols, n_connects)
        # update (0, 0)
        row, col, marker = 0, 0, Marker.CIRCLE
        assert board.col_count.sum(axis=None) == 0
        board.update_col_count(marker, row, col)
        assert board.col_count[marker, col, 0] == 1
        # update (1, 1)
        board.restart()
        row, col, marker = 1, 1, Marker.CROSS
        assert board.col_count.sum(axis=None) == 0
        board.update_col_count(marker, row, col)
        assert board.col_count[marker, col, 0] == 1
        assert board.col_count[marker, col, 1] == 1
        # update (2, 2)
        board.restart()
        row, col, marker = 2, 2, Marker.CIRCLE
        assert board.col_count.sum(axis=None) == 0
        board.update_col_count(marker, row, col)
        assert board.col_count[marker, col, 0] == 1
        assert board.col_count[marker, col, 1] == 1
        # update (3, 2)
        board.restart()
        row, col, marker = 3, 2, Marker.CROSS
        assert board.col_count.sum(axis=None) == 0
        board.update_col_count(marker, row, col)
        assert board.col_count[marker, col, 0] == 0
        assert board.col_count[marker, col, 1] == 1

    def test_3x3x3_update_l2r_diag_count(self):
        n_rows, n_cols, n_connects = 3, 3, 3
        board = Board2d(n_rows, n_cols, n_connects)
        # update (0, 0)
        row, col, marker = 0, 0, Marker.CIRCLE
        assert board.l2r_diag_count.sum(axis=None) == 0
        board.update_l2r_diag_count(marker, row, col)
        assert board.l2r_diag_count[marker, 0, 0] == 1
        # update (1, 1)
        row, col, marker = 1, 1, Marker.CROSS
        board.update_l2r_diag_count(marker, row, col)
        assert board.l2r_diag_count[marker, 0, 0] == 1
        # update (2, 2)
        row, col, marker = 2, 2, Marker.CIRCLE
        board.update_l2r_diag_count(marker, row, col)
        assert board.l2r_diag_count[marker, 0, 0] == 2
        # update (0, 1), CROSS count stay the same from (1, 1)
        row, col, marker = 0, 1, Marker.CROSS
        board.update_l2r_diag_count(marker, row, col)
        assert board.l2r_diag_count[marker, 0, 0] == 1

    def test_4x3x3_update_l2r_diag_count(self):
        n_rows, n_cols, n_connects = 4, 3, 3
        board = Board2d(n_rows, n_cols, n_connects)
        # update (0, 0)
        row, col, marker = 0, 0, Marker.CIRCLE
        assert board.l2r_diag_count.sum(axis=None) == 0
        board.update_l2r_diag_count(marker, row, col)
        assert board.l2r_diag_count[marker, 0, 0] == 1
        # update (1, 1)
        board.restart()
        row, col, marker = 1, 1, Marker.CROSS
        assert board.l2r_diag_count.sum(axis=None) == 0
        board.update_l2r_diag_count(marker, row, col)
        assert board.l2r_diag_count[marker, 0, 0] == 1
        assert board.l2r_diag_count[marker, 0, 1] == 0
        # update (1, 0)
        board.restart()
        row, col, marker = 1, 0, Marker.CIRCLE
        assert board.l2r_diag_count.sum(axis=None) == 0
        board.update_l2r_diag_count(marker, row, col)
        assert board.l2r_diag_count[marker, 0, 0] == 0
        assert board.l2r_diag_count[marker, 0, 1] == 1
        # update (2, 0)
        board.restart()
        row, col, marker = 2, 0, Marker.CROSS
        assert board.l2r_diag_count.sum(axis=None) == 0
        board.update_l2r_diag_count(marker, row, col)
        assert board.l2r_diag_count[marker, 0, 0] == 0
        assert board.l2r_diag_count[marker, 0, 1] == 0

    def test_4x4x3_update_l2r_diag_count(self):
        n_rows, n_cols, n_connects = 4, 4, 3
        board = Board2d(n_rows, n_cols, n_connects)
        # update (0, 0)
        row, col, marker = 0, 0, Marker.CIRCLE
        assert board.l2r_diag_count.sum(axis=None) == 0
        board.update_l2r_diag_count(marker, row, col)
        assert board.l2r_diag_count[marker, 0, 0] == 1
        # update (1, 1)
        board.restart()
        row, col, marker = 1, 1, Marker.CROSS
        assert board.l2r_diag_count.sum(axis=None) == 0
        board.update_l2r_diag_count(marker, row, col)
        assert board.l2r_diag_count[marker, 0, 0] == 1
        assert board.l2r_diag_count[marker, 1, 1] == 1
        # update (1, 0)
        board.restart()
        row, col, marker = 1, 0, Marker.CIRCLE
        assert board.l2r_diag_count.sum(axis=None) == 0
        board.update_l2r_diag_count(marker, row, col)
        assert board.l2r_diag_count[marker, 0, 0] == 0
        assert board.l2r_diag_count[marker, 0, 1] == 1
        # update (2, 0)
        board.restart()
        row, col, marker = 2, 0, Marker.CROSS
        assert board.l2r_diag_count.sum(axis=None) == 0
        board.update_l2r_diag_count(marker, row, col)
        assert board.l2r_diag_count[marker, 0, 0] == 0
        assert board.l2r_diag_count[marker, 0, 1] == 0
        # update (0, 1)
        board.restart()
        row, col, marker = 0, 1, Marker.CIRCLE
        assert board.l2r_diag_count.sum(axis=None) == 0
        board.update_l2r_diag_count(marker, row, col)
        assert board.l2r_diag_count[marker, 1, 0] == 1
        assert board.l2r_diag_count[marker, 0, 1] == 0
        assert board.l2r_diag_count[marker, 1, 1] == 0

    def test_3x3x3_update_r2l_diag_count(self):
        n_rows, n_cols, n_connects = 3, 3, 3
        board = Board2d(n_rows, n_cols, n_connects)
        # update (0, 0)
        row, col, marker = 0, 0, Marker.CIRCLE
        assert board.r2l_diag_count.sum(axis=None) == 0
        board.update_r2l_diag_count(marker, row, col)
        assert board.r2l_diag_count[marker, 0, 0] == 0
        # update (0, 2)
        board.restart()
        row, col, marker = 0, 2, Marker.CROSS
        assert board.r2l_diag_count.sum(axis=None) == 0
        board.update_r2l_diag_count(marker, row, col)
        assert board.r2l_diag_count[marker, 0, 0] == 1
        # update (1, 1)
        board.restart()
        row, col, marker = 1, 1, Marker.CROSS
        assert board.r2l_diag_count.sum(axis=None) == 0
        board.update_r2l_diag_count(marker, row, col)
        assert board.r2l_diag_count[marker, 0, 0] == 1
        # update (2, 2)
        board.restart()
        row, col, marker = 2, 2, Marker.CIRCLE
        assert board.r2l_diag_count.sum(axis=None) == 0
        board.update_r2l_diag_count(marker, row, col)
        assert board.r2l_diag_count[marker, 0, 0] == 0
        # update (2, 0)
        board.restart()
        row, col, marker = 2, 0, Marker.CROSS
        assert board.r2l_diag_count.sum(axis=None) == 0
        board.update_r2l_diag_count(marker, row, col)
        assert board.r2l_diag_count[marker, 0, 0] == 1

    def test_4x4x3_update_r2l_diag_count(self):
        n_rows, n_cols, n_connects = 4, 4, 3
        board = Board2d(n_rows, n_cols, n_connects)
        # update (0, 0)
        row, col, marker = 0, 0, Marker.CIRCLE
        assert board.r2l_diag_count.sum(axis=None) == 0
        board.update_r2l_diag_count(marker, row, col)
        assert board.r2l_diag_count[marker, 0, 0] == 0
        # update (0, 2)
        board.restart()
        row, col, marker = 0, 2, Marker.CROSS
        assert board.r2l_diag_count.sum(axis=None) == 0
        board.update_r2l_diag_count(marker, row, col)
        assert board.r2l_diag_count[marker, 0, 0] == 1
        # update (1, 1)
        board.restart()
        row, col, marker = 1, 1, Marker.CIRCLE
        assert board.r2l_diag_count.sum(axis=None) == 0
        board.update_r2l_diag_count(marker, row, col)
        assert board.r2l_diag_count[marker, 0, 0] == 1
        # update (1, 2)
        board.restart()
        row, col, marker = 1, 2, Marker.CROSS
        assert board.r2l_diag_count.sum(axis=None) == 0
        board.update_r2l_diag_count(marker, row, col)
        assert board.r2l_diag_count[marker, 1, 0] == 1
        assert board.r2l_diag_count[marker, 0, 1] == 1
        # update (3, 1)
        board.restart()
        row, col, marker = 3, 1, Marker.CIRCLE
        assert board.r2l_diag_count.sum(axis=None) == 0
        board.update_r2l_diag_count(marker, row, col)
        assert board.r2l_diag_count[marker, 0, 0] == 0
        assert board.r2l_diag_count[marker, 1, 0] == 0
        assert board.r2l_diag_count[marker, 1, 1] == 1
