from enum import Enum
from abc import ABC, abstractmethod
from . import utils
import logging, logging.config
from .board import *
from .player import *
import numpy as np


__all__ = [
    'GameParameter',
    'GameBasic'
]


class GameParameter(Enum):
    N_ROUNDS = 1
    FIRST_TO = 2
    BOARD_DIM = 3


class Game(ABC):
    def __init__(self, players, game_configs, view):
        self.logger = utils.make_logger(Game.__name__)
        self.players = players
        self.marker2player = dict()
        self.game_configs = game_configs
        self.board = None
        self.view = view
        self._marker = Marker.CIRCLE
        self._winner = None

    #------------------------------------------------------------ 
    # Properties
    #------------------------------------------------------------ 
    @property
    def marker(self):
        return self._marker

    @marker.setter
    def marker(self, m):
        raise NotImplementedError('Cannot set current marker!')

    @property
    def winner(self):
        return self._winner

    @winner.setter
    def winner(self, w):
        raise NotImplementedError('Cannot set game winner!')

    #------------------------------------------------------------ 
    # Abstract methods
    #------------------------------------------------------------ 
    def setup(self):
        for marker, player in zip(Marker, self.players):
            player.board = self.board
            player.marker = marker
            self.marker2player[marker] = player
        self.logger.debug('marker2player: {}'.format(self.marker2player))

    def start_board(self):
        while self.board.state == BoardState.ONGOING:
            self.logger.debug('Next round...')
            cur_player = self.marker2player[self._marker]

            if cur_player.is_real:
                loc = self.prompt_move(self._marker)
            else:
                loc = cur_player.get_move()

            move = Cell(self._marker, loc)
            self.board.mark_cell(move.content, move.loc)

            if not cur_player.is_real:
                msg = '{} marked {!r} at {}'
                msg = msg.format(cur_player.name,
                                 cur_player.marker,
                                 loc)
                self.view.display_msg(msg)

            # increment marker
            n_markers = len(Marker)
            self.logger.debug('no. of markers: {}'.format(n_markers))
            self._marker = Marker((self._marker + 1) % n_markers)
        self.end_board()

    def end_board(self):
        # set winner if needed
        marker_int = self.board.state - BoardState.CIRCLE_WIN
        if marker_int >= 0:
            marker = Marker(marker_int)
            self._winner = self.marker2player[marker]

    def start(self):
        self.setup()
        welcome_msg = 'Welcome to Tic Tac Toe'
        self.view.display_msg(welcome_msg)
        self.start_board()
        self.end()

    def end(self):
        self.logger.info('Game end')
        if self.winner is None:
            msg = 'Draw game.'
        else:
            msg = '{!s} ({!r}) has won.'
            msg = msg.format(self.winner.name, self.winner.marker)
        self.view.display_msg(msg)

    def prompt_move(self, marker):
        msg = 'Enter move coordinate ({}): '
        msg = msg.format(self.board.CellLocation.COORDINATE_FORMAT)
        loc = None
        while loc is None or not self.board.is_cell_empty(loc):
            loc_str = self.view.get_input(msg)
            try:
                loc = self.board.CellLocation.parse(loc_str)
            except:
                self.logger.error('Parse location error: {}'.format(loc))
                loc = None
                continue
            is_empty = self.board.is_cell_empty(loc)
            self.logger.debug('{} is empty: {}'.format(loc, is_empty))
        return loc


class GameBasic(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score = {marker:0 for marker in Marker}
        self.total_round = 0

    def setup(self):
        n_rows = self.game_configs[GameParameter.BOARD_DIM]
        n_cols = self.game_configs[GameParameter.BOARD_DIM]
        self.board = Board2d(n_rows, n_cols)
        self.board.register_observer(self.view)
        super().setup()

    def __reached_max_round(self):
        # check if all the scores are the same
        score_list = np.asarray(list(self.score.values()))
        draw = (score_list == score_list[0]).all()
        if not draw:
            # compute the winner
            max_score = -1
            winner = None
            for marker,player in self.marker2player.items():
                score = self.score[marker]
                self._winner = player if score > max_score else self._winner
                max_score = score if score > max_score else max_score

    def start_board(self):
        round_msg = 'Round {}/{}'.format(self.total_round, 
                                         self.game_configs[GameParameter.N_ROUNDS])
        self.view.display_msg(round_msg)
        super().start_board()

    def end_board(self):
        self.total_round += 1
        # increment winner's score
        marker_int = self.board.state - BoardState.CIRCLE_WIN
        if marker_int >= 0:
            marker = Marker(marker_int)
            self.score[marker] += 1
            if self.score[marker] >= self.game_configs[GameParameter.FIRST_TO]:
                self._winner = self.marker2player[marker]
                return
            msg = '{} ({!r}) wins round {}'
            msg = msg.format(self.marker2player[marker].name,
                             self.marker,
                             self.total_round - 1)
            self.view.display_msg(msg)
        else:
            msg = 'Draw round {}'.format(self.total_round - 1)
            self.view.display_msg(msg)

        maxed_rounds = self.total_round >= self.game_configs[GameParameter.N_ROUNDS]
        if maxed_rounds:
            self.__reached_max_round()
            return

        # game not finished yet, restart board
        self.board.restart()
        self.start_board()

    def start(self):
        self.setup()
        welcome_msg = 'Welcome to Tic Tac Toe'
        self.view.display_msg(welcome_msg)
        self.start_board()
        self.end()

    def end(self):
        self.logger.info('Game end')
        if self.winner is None:
            msg = 'Draw game after {} games.'.format(self.total_round)
        else:
            msg = '{!s} ({!r}) has won {} rounds out of {} games.'
            msg = msg.format(self.winner.name, 
                             self.winner.marker,
                             self.score[self.winner.marker],
                             self.total_round)
        self.view.display_msg(msg)

    def mark_cell(self, marker, loc):
        is_marked = self.board.mark_cell(marker, loc)
        return is_marked
