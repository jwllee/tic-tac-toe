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
        return reverse('xo:game', kwargs={'pk': self.pk})

    @property
    def empty_indexes(self):
        return board_utils.get_empty_indexes(
            self.board_x, self.board_o, self.n_cells)

    @property
    def n_cells(self):
        return self.n_rows * self.n_cols

    @property
    def board_str(self):
        return board_utils.get_board_str(
            self.board_x, self.board_o, self.n_cells)

    @property
    def board_mat(self):
        return board_utils.get_board_mat(
            self.board_x, self.board_o, self.n_rows, self.n_cols)

    @property
    def full_state(self):
        return (1 << self.n_cells) - 1

    @property
    def is_filled(self):
        return board_utils.is_filled(
            self.board_x, self.board_o, self.full_state)

    @property
    def next_player(self):
        return board_utils.get_next_player(
            self.board_x, self.board_o, self.n_cells)

    def is_next_player_human(self):
        if self.next_player == board_utils.MARKER_O:
            return self.player_o == 'human'
        else:
            return self.player_x == 'human'

    @property
    def is_game_over(self):
        is_over =  board_utils.is_game_over(
            self.board_x, self.board_o, self.n_rows, self.n_cols, self.n_connects)
        # print('Game {} is over: {}'.format(self.pk, is_over))
        return is_over

    def is_empty(self, index):
        return board_utils.is_empty(
            self.board_x, self.board_o, index)

    def add_cross(self, index):
        flag = 1 << index
        self.board_x |= flag

    def add_circle(self, index):
        flag = 1 << index 
        self.board_o |= flag

    def play_auto(self):
        if self.is_game_over:
            return 

        has_human = self.player_x == 'human' or self.player_o == 'human'

        if has_human:
            next_player = self.next_player
            player = self.player_x if next_player == MARKER_X else self.player_o

            if player == 'human':
                return 

            player_obj = get_player(player)
            self.play(player_obj.play(self))
        else:
            while not self.is_game_over:
                next_player = self.next_player
                player = self.player_x if next_player  == MARKER_X else self.player_o
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


class BoardState(models.Model):
    """All the board state is cached with their utility value assuming that it is at a max layer
    """
    # goes up to 2^31 - 1, so 5x5 has 25 cells is still ok
    board_x = models.PositiveIntegerField(default=0)
    board_o = models.PositiveIntegerField(default=0)

    n_rows = models.IntegerField(default=3)
    n_cols = models.IntegerField(default=3)
    n_connects = models.IntegerField(default=3)

    depth = models.IntegerField(default=0)
    flag = models.IntegerField(default=board_utils.EXACT)
    value = models.IntegerField()

    def __repr__(self):
        repr_ = 'BoardState({}, {}, {}, "{}", {}, {}, {})'
        flag_str = board_utils.flag2str(self.flag)
        repr_ = repr_.format(self.n_rows, 
                             self.n_cols,
                             self.n_connects,
                             self.board_str,
                             self.depth,
                             self.value,
                             flag_str)
        return repr_

    def __str__(self):
        return str(repr(self))

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

    @classmethod
    def cache(cls, board_x, board_o, n_rows, n_cols, n_connects, depth, value, flag):
        # cache if it's not already there
        results = BoardState.objects.filter(
            n_rows__exact=n_rows,
            n_cols__exact=n_cols,
            n_connects__exact=n_connects,
            board_x__exact=board_x,
            board_o__exact=board_o,
            flag__exact=flag,
            depth__gte=depth,
        )

        if len(results):
            return
        
        BoardState.objects.create(
            board_x=board_x,
            board_o=board_o,
            n_rows=n_rows,
            n_cols=n_cols,
            n_connects=n_connects,
            flag=flag,
            value=value,
            depth=depth,
        )

    @classmethod
    def get_cache(cls, board_x, board_o, n_rows, n_cols, n_connects):
        cache = None
        results = BoardState.objects.filter(
            n_rows__exact=n_rows,
            n_cols__exact=n_cols,
            n_connects__exact=n_connects,
            board_x__exact=board_x,
            board_o__exact=board_o,
        ).order_by('flag', '-depth')
        len_ = len(results)
        if len_ > 0:
            cache = results[0]
        return cache
