from tictac import view, utils
from tictac import board as board_mod
import pytest, io


@pytest.fixture
def make_board2d():
    def _make_board2d(n_rows, n_cols):
        board = board_mod.Board2d(n_rows, n_cols)
        return board
    return _make_board2d


class TestTextBoard2dDisplayer:
    def test_init(self):
        displayer = view.TextBoard2dDisplayer()
        expected = view.TextBoard2dDisplayer
        actual = displayer
        utils.assert_isinstance('displayer', expected, actual)

    def test_display_empty_2x2_board_at_stdout(self, make_board2d):
        board = make_board2d(2, 2)
        displayer = view.TextBoard2dDisplayer()
        out = io.StringIO()
        displayer.display(board, f=out)
        line = out.getvalue()
        expected = 'Board\n{empty}{empty}\n{empty}{empty}\n'
        expected = expected.format(empty=view.TextBoard2dDisplayer.EMPTY)
        assert line == expected

    def test_display_empty_3x3_board_at_stdout(self, make_board2d):
        board = make_board2d(3, 3)
        displayer = view.TextBoard2dDisplayer()
        out = io.StringIO()
        displayer.display(board, f=out)
        line = out.getvalue()
        expected = 'Board\n{emp}{emp}{emp}\n{emp}{emp}{emp}\n{emp}{emp}{emp}\n'
        expected = expected.format(emp=view.TextBoard2dDisplayer.EMPTY)
        assert line == expected

