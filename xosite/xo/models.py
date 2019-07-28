from django.db import models
from django.shortcuts import reverse


from .players import get_player
from . import board_utils


MARKER_X = 'X'
MARKER_O = 'O'


class Game(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # goes up to 2^31 - 1, so 5x5 has 25 cells is still ok
    board_x = models.PositiveIntegerField(default=0)
    board_o = models.PositiveIntegerField(default=0)

    player_x = models.CharField(max_length=64)
    player_o = models.CharField(max_length=64)

    n_rows = models.IntegerField(default=3)
    n_cols = models.IntegerField(default=3)
    n_connects = models.IntegerField(default=3)
    is_kriegspiel = models.BooleanField(default=False)

    def __repr__(self):
        repr_ = 'Game({}, {}, {}, "{}")'
        repr_ = repr_.format(self.n_rows, 
                             self.n_cols, 
                             self.n_connects,
                             self.board_str)
        return repr_

    def __str__(self):
        return str(repr(self))

    def get_absolute_url(self):
        # todo: 3x3 has a different url to 4x4 game
        return reverse('xo:game', kwargs={'pk': self.pk})

    @property
    def empty_indexes(self):
        indexes = []
        for i in range(self.n_cells):
            flag = 1 << i
            has_x = self.board_x & flag
            has_o = self.board_o & flag
            if not (has_x or has_o):
                indexes.append(i)
        return indexes

    @property
    def n_cells(self):
        return self.n_rows * self.n_cols

    @property
    def board_str(self):
        s = ''
        for i in range(self.n_cells):
            v = ' '
            flag = 1 << i
            has_x = self.board_x & flag
            has_o = self.board_o & flag
            if has_x:
                v = MARKER_X
            if has_o:
                v = MARKER_O
            s += v
        return s

    @property
    def full_state(self):
        return (1 << self.n_cells) - 1

    @property
    def is_filled(self):
        current_state = self.board_o | self.board_x
        filled = (current_state & self.full_state) == self.full_state
        return filled

    @property
    def next_player(self):
        n_x = 0
        n_o = 0
        board_x = self.board_x
        board_o = self.board_o

        for i in range(self.n_cells):
            n_x += board_x & 0b1
            n_o += board_o & 0b1
            board_x >>= 1
            board_o >>= 1

        err_msg = 'Board has {} X and {} O'
        err_msg = err_msg.format(n_x, n_o)
        assert abs(n_x - n_o) == 1 or n_x == n_o, err_msg
        player = MARKER_O if n_o < n_x else MARKER_X

        return player

    @property
    def is_game_over(self):
        # check for drawn first
        board_win = board_utils.get_board_wins(self.n_rows, self.n_cols, self.n_connects)
        # None for ongoing
        result = None
        for win in board_win:
            x_win = (self.board_x & win) == win
            o_win = (self.board_o & win) == win
            if x_win:
                result = 'X'
                break
            elif o_win:
                result = 'O'
                break
        if result is None and self.is_filled:
            result = ' '
        return result

    def is_empty(self, index):
        flag = 1 << index
        has_x = self.board_x & flag
        has_o = self.board_o & flag
        return (has_x | has_o) == 0

    def add_cross(self, index):
        flag = 1 << index
        self.board_x |= flag

    def add_circle(self, index):
        flag = 1 << index 
        self.board_o |= flag

    def play_auto(self):
        while not self.is_game_over:
            next_player = self.next_player
            player = self.player_x if next_player  == MARKER_X else self.player_o

            if player == 'human':
                return
            
            player_obj = get_player(player)
            self.play(player_obj.play(self))

    def play(self, index):
        info_msg = 'Player {} playing index {} at game {}'
        info_msg = info_msg.format(self.next_player, index, self.pk)
        print(info_msg)

        if index < 0 or index >= self.n_cells:
            err_msg = 'Invalid board index {} not in [{}, {})'
            err_msg = err_msg.format(index, 0, self.n_cells)
            raise IndexError(err_msg)

        if not self.is_empty(index):
            err_msg = 'Cell is not empty at index {}'
            err_msg = err_msg.format(index)
            raise ValueError(err_msg)

        if self.next_player == MARKER_X:
            self.add_cross(index)
        else:
            self.add_circle(index)
