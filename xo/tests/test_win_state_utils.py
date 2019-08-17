from django.test import TestCase
from xo import win_state_utils as utils


class WinStateUtilsTest(TestCase):
    def test_compute_win_state_row_3x3x3(self):
        n_rows, n_cols, n_connects = 3, 3, 3
        wins = utils.compute_win_state_row(n_rows, n_cols, n_connects)

        expected = [
            0b000000111,    # rows
            0b000111000,
            0b111000000,
        ]

        wins = sorted(wins)
        expected = sorted(expected)

        assert wins == expected

    def test_compute_win_state_row_3x4x3(self):
        n_rows, n_cols, n_connects = 3, 4, 3
        wins = utils.compute_win_state_row(n_rows, n_cols, n_connects)

        expected = [
            0b000000000111,
            0b000000001110,
            0b000001110000,
            0b000011100000,
            0b011100000000,
            0b111000000000,
        ]

        wins = sorted(wins)
        expected = sorted(expected)

        assert wins == expected

    def test_compute_win_state_col_3x3x3(self):
        n_rows, n_cols, n_connects = 3, 3, 3
        wins = utils.compute_win_state_col(n_rows, n_cols, n_connects)

        expected = [
            0b001001001,    # columns
            0b010010010,
            0b100100100,
        ]

        wins = sorted(wins)
        expected = sorted(expected)

        assert wins == expected

    def test_compute_win_state_col_4x4x4(self):
        n_rows, n_cols, n_connects = 4, 4, 4
        wins = utils.compute_win_state_col(n_rows, n_cols, n_connects)

        expected = [
            0b0001000100010001, # columns
            0b0010001000100010,
            0b0100010001000100,
            0b1000100010001000, 
        ]

        wins = sorted(wins)
        expected = sorted(expected)

        assert wins == expected
    
    def test_compute_win_state_col_4x4x3(self):
        n_rows, n_cols, n_connects = 4, 4, 3
        wins = utils.compute_win_state_col(n_rows, n_cols, n_connects)

        expected = [
            0b0000000100010001, # columns
            0b0001000100010000, 
            0b0000001000100010,
            0b0010001000100000,
            0b0000010001000100,
            0b0100010001000000,
            0b0000100010001000, 
            0b1000100010000000, 
        ]

        wins = sorted(wins)
        expected = sorted(expected)

        assert wins == expected

    def test_compute_win_state_col_5x5x5(self):
        n_rows, n_cols, n_connects = 5, 5, 5
        wins = utils.compute_win_state_col(n_rows, n_cols, n_connects)

        expected = [
            0b0000100001000010000100001, # columns
            0b0001000010000100001000010,
            0b0010000100001000010000100,
            0b0100001000010000100001000,
            0b1000010000100001000010000,
        ]

        wins = sorted(wins)
        expected = sorted(expected)

        assert wins == expected
