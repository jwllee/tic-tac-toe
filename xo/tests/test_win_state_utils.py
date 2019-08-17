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

    def test_compute_win_state_str_row_3x4x3(self):
        n_rows, n_cols, n_connects = 3, 4, 3
        wins = utils.compute_win_state_str_row(n_rows, n_cols, n_connects)

        expected = [
            '000000000111',
            '000000001110',
            '000001110000',
            '000011100000',
            '011100000000',
            '111000000000'
        ]
        
        wins = sorted(wins)
        expected = sorted(expected)

        assert_msg = '{} != {}'.format(expected, wins)
        assert expected == wins, assert_msg

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

    def test_compute_win_state_str_col_4x3x3(self):
        n_rows, n_cols, n_connects = 4, 3, 3
        wins = utils.compute_win_state_str_col(n_rows, n_cols, n_connects)

        expected = [
            '100100100000',
            '010010010000',
            '001001001000',
            '000100100100',
            '000010010010',
            '000001001001',
        ]
        
        wins = sorted(wins)
        expected = sorted(expected)

        assert_msg = '{} != {}'.format(expected, wins)
        assert expected == wins, assert_msg

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

    def test_compute_win_state_str_diag_l2r_3x3x3(self):
        n_rows, n_cols, n_connects = 3, 3, 3
        wins = utils.compute_win_state_str_diag_l2r(n_rows, n_cols, n_connects)

        expected = [
            '100010001'
        ]

        assert_msg = '{} != {}'.format(expected, wins)
        assert expected == wins, assert_msg

    def test_compute_win_state_str_diag_l2r_4x4x4(self):
        n_rows, n_cols, n_connects = 4, 4, 4
        wins = utils.compute_win_state_str_diag_l2r(n_rows, n_cols, n_connects)

        expected = [
            '1000010000100001', # diagonals
        ]

        assert_msg = '{} != {}'.format(expected, wins)
        assert expected == wins, assert_msg

    def test_compute_win_state_str_diag_l2r_5x5x5(self):
        n_rows, n_cols, n_connects = 5, 5, 5
        wins = utils.compute_win_state_str_diag_l2r(n_rows, n_cols, n_connects)

        expected = [
            '1000001000001000001000001', # diagonals
        ]

        assert_msg = '{} != {}'.format(expected, wins)
        assert expected == wins, assert_msg

    def test_compute_win_state_str_diag_l2r_4x4x3(self):
        n_rows, n_cols, n_connects = 4, 4, 3
        wins = utils.compute_win_state_str_diag_l2r(n_rows, n_cols, n_connects)

        expected = [
            '0000010000100001', # diagonals
            '1000010000100000', 
            '0000100001000010',
            '0100001000010000',
        ]

        wins = sorted(wins)
        expected = sorted(expected)

        assert_msg = '{} != {}'.format(expected, wins)
        assert expected == wins, assert_msg

    def test_compute_win_state_str_diag_r2l_3x3x3(self):
        n_rows, n_cols, n_connects = 3, 3, 3
        wins = utils.compute_win_state_str_diag_r2l(n_rows, n_cols, n_connects)

        expected = [
            '001010100'
        ]

        wins = sorted(wins)
        expected = sorted(expected)

        assert_msg = '{} != {}'.format(expected, wins)
        assert expected == wins, assert_msg

    def test_compute_win_state_str_diag_r2l_4x4x4(self):
        n_rows, n_cols, n_connects = 4, 4, 4
        wins = utils.compute_win_state_str_diag_r2l(n_rows, n_cols, n_connects)

        expected = [
            '0001001001001000',
        ]

        wins = sorted(wins)
        expected = sorted(expected)

        assert_msg = '{} != {}'.format(expected, wins)
        assert expected == wins, assert_msg

    def test_compute_win_state_str_diag_r2l_4x4x3(self):
        n_rows, n_cols, n_connects = 4, 4, 3
        wins = utils.compute_win_state_str_diag_r2l(n_rows, n_cols, n_connects)

        expected = [
            '0000000100100100',
            '0000001001001000',
            '0001001001000000',
            '0010010010000000',
        ]

        wins = sorted(wins)
        expected = sorted(expected)

        assert_msg = '{} != {}'.format(expected, wins)
        assert expected == wins, assert_msg
