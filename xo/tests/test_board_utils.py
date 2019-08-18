from django.test import TestCase
from xo import board_utils as utils


def assert_reflected(expected, actual, n_cells):
    expected_str = utils.get_board_str(expected, 0, n_cells)
    reflected_str = utils.get_board_str(actual, 0, n_cells)
    assert_msg = '"{}" != "{}"'.format(expected_str, reflected_str)
    assert expected == actual, assert_msg


class BoardUtilsTest(TestCase):
    def test_reflect_y_3x3x3(self):
        n_rows, n_cols = 3, 3
        n_cells = n_rows * n_cols

        board = 0b000000001
        reflected = utils.reflect_y(board, n_rows, n_cols)
        expected = 0b000000100
        assert_reflected(expected, reflected, n_cells)

        board = 0b100100100
        reflected = utils.reflect_y(board, n_rows, n_cols)
        expected = 0b001001001
        assert_reflected(expected, reflected, n_cells)

    def test_reflect_x_3x3x3(self):
        n_rows, n_cols = 3, 3
        n_cells = n_rows * n_cols

        board = 0b100000000
        reflected = utils.reflect_x(board, n_rows, n_cols)
        expected = 0b000000100
        assert_reflected(expected, reflected, n_cells)

        board = 0b111000000
        reflected = utils.reflect_x(board, n_rows, n_cols)
        expected = 0b000000111
        assert_reflected(expected, reflected, n_cells)





