from django.test import TestCase


from .models import Game


class GameModelTests(TestCase):
    def test_3x3_filled_board_is_drawn(self):
        game = Game(n_rows=3, n_cols=3)
        # 0 - 4 are with o
        game.board_o = 0b000001111
        # 5 - 8 are with x
        game.board_x = 0b111110000
        self.assertIs(game.is_filled, True)

    def test_3x3_full_state(self):
        game = Game(n_rows=3, n_cols=3)
        expected = 0b111111111
        self.assertEqual(game.full_state, expected)

    def test_4x4_full_state(self):
        game = Game(n_rows=4, n_cols=4)
        expected = 0b1111111111111111
        self.assertEqual(game.full_state, expected)

    def test_3x4_full_state(self):
        game = Game(n_rows=3, n_cols=4)
        expected = 0b111111111111
        self.assertEqual(game.full_state, expected)

    def test_4x3_full_state(self):
        game = Game(n_rows=4, n_cols=3)
        expected = 0b111111111111
        self.assertEqual(game.full_state, expected)

    def test_3x3_add_cross(self):
        game = Game(n_rows=3, n_cols=3)
        game.add_cross(0)
        self.assertEqual(game.board_x, 0b000000001)

        game.add_cross(8)
        self.assertEqual(game.board_x, 0b100000001)

        game.add_cross(4)
        self.assertEqual(game.board_x, 0b100010001)

    def test_3x3_add_circle(self):
        game = Game(n_rows=3, n_cols=3)
        game.add_circle(0)
        self.assertEqual(game.board_o, 0b000000001)

        game.add_circle(8)
        self.assertEqual(game.board_o, 0b100000001)

        game.add_circle(4)
        self.assertEqual(game.board_o, 0b100010001)

    def test_3x3_is_empty(self):
        game = Game(n_rows=3, n_cols=3)
        game.add_cross(8)
        self.assertIs(game.is_empty(8), False)
        self.assertIs(game.is_empty(4), True)

    def test_3x3_board_str(self):
        game = Game(n_rows=3, n_cols=3)
        game.add_cross(0)
        game.add_cross(8)
        game.add_circle(4)
        board_str = game.board_str
        expected = 'X   O   X'
        self.assertEqual(board_str, expected)
