from django.db import models
from django.shortcuts import reverse


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
                v = 'X'
            if has_o:
                v = 'O'
            s += v
        return s

    @property
    def full_state(self):
        return (1 << self.n_cells) - 1

    @property
    def is_drawn(self):
        current_state = self.board_o | self.board_x
        drawn = (current_state & self.full_state) == self.full_state
        return drawn

    def is_empty(self, row, col):
        flag = 1 << (row * self.n_cols + col)
        has_x = self.board_x & flag
        has_o = self.board_o & flag
        return (has_x | has_o) == 0

    def add_cross(self, row, col):
        flag = 1 << (row * self.n_cols + col)
        self.board_x |= flag

    def add_circle(self, row, col):
        flag = 1 << (row * self.n_cols + col)
        self.board_o |= flag

    def play_auto(self):
        print('Playing auto')

    def play(self, index):
        print('Playing')
