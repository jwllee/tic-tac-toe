import pytest
from tictac.board import *


@pytest.fixture
def make_board2d():
    def _make_board2d(n_rows, n_cols):
        board = Board2d(n_rows, n_cols)
        return board
    return _make_board2d


class TestBoard2d:
    @pytest.fixture(scope='function')
    def board_3x3_circle_winner_r2l(self, make_board2d):
        board = make_board2d(3, 3)
        board.board[0, 2] = Marker.CIRCLE
        board.board[1, 1] = Marker.CIRCLE
        board.board[2, 0] = Marker.CIRCLE
        return board

    @pytest.fixture(scope='function')
    def board_3x3_circle_winner_l2r(self, make_board2d):
        board = make_board2d(3, 3)
        board.board[0, 0] = Marker.CIRCLE
        board.board[1, 1] = Marker.CIRCLE
        board.board[2, 2] = Marker.CIRCLE
        return board

    def test_3x3_circle_winner_l2r_get_diag_count(self, board_3x3_circle_winner_l2r):
        board = board_3x3_circle_winner_l2r
        diag_dict = board.get_diag_count(0)
        err_msg = 'Player "{!r}" should have {} counts, diag_dict: {}'
        assert diag_dict[Marker.CROSS] == 0, err_msg.format(Marker.CROSS, 0, diag_dict)
        assert diag_dict[Marker.CIRCLE] == 3, err_msg.format(Marker.CIRCLE, 3, diag_dict)

    def test_3x3_circle_winner_l2r_check_diagonal(self, board_3x3_circle_winner_l2r):
        board = board_3x3_circle_winner_l2r
        has_winner = board.check_diagonal()
        assert has_winner, 'Should have returned "{!r}" as winner'.format(Marker.CIRCLE)

    def test_3x3_circle_winner_r2l_get_diag_count(self, board_3x3_circle_winner_r2l):
        board = board_3x3_circle_winner_r2l
        diag_dict = board.get_diag_count(board.n_rows - 1, False)
        err_msg = 'Player "{!r}" should have {} counts, diag_dict: {}'
        assert diag_dict[Marker.CROSS] == 0, err_msg.format(Marker.CROSS, 0, diag_dict)
        assert diag_dict[Marker.CIRCLE] == 3, err_msg.format(Marker.CIRCLE, 3, diag_dict)

    def test_3x3_circle_winner_r2l_check_diagonal(self, board_3x3_circle_winner_r2l):
        board = board_3x3_circle_winner_r2l
        has_winner = board.check_diagonal(False)
        assert has_winner, 'Should have returned "{!r}" as winner'.format(Marker.CIRCLE)
