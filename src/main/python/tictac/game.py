from enum import Enum
from abc import ABC, abstractmethod
from . import utils
import logging, logging.config
from .board import *
from .player import *
import numpy as np

from utils import NotificationKey, NotificationType


__all__ = [
    'GameParameter',
    'GameBasic'
]


class GameParameter(Enum):
    N_ROUNDS = 1
    FIRST_TO = 2
    BOARD_DIM = 3


class Game(ABC):
    def __init__(self, board, players, game_configs):
        self.logger = utils.make_logger(Game.__name__)
        self.players = players
        self.marker2player = dict()
        self.game_configs = game_configs
        self.board = board
        self._marker = Marker.CIRCLE
        self.observers = list()

    #------------------------------------------------------------ 
    # Observer pattern
    #------------------------------------------------------------ 
    def register_observer(self, obs):
        self.observers.append(obs)

    def remove_observer(self, obs):
        self.observers.remove(obs)

    def notify_observers(self, type_, data):
        for obs in self.observers:
            obs.update(type_, data)

    #------------------------------------------------------------ 
    # Properties
    #------------------------------------------------------------ 
    @property
    def cur_marker(self):
        return self._marker

    @cur_marker.setter
    def cur_marker(self, m):
        raise NotImplementedError('Cannot set current marker!')

    @property
    def cur_player(self):
        return self.marker2player[self.cur_marker]

    @cur_player.setter
    def cur_player(self, p):
        raise NotImplementedError('Cannot set current player!')

    @property
    def ongoing(self):
        return self.board.state == BoardState.ONGOING

    @ongoing.setter
    def ongoing(self, o):
        raise NotImplementedError('Cannot set game ongoing state!')

    @property
    def winner(self):
        marker_int = self.board.state - BoardState.CIRCLE_WIN
        winner = None
        if marker_int >= 0:
            marker = Marker(marker_int)
            winner = self.marker2player[marker]
        return winner

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
        self._marker = Marker.CIRCLE
        self.logger.debug('marker2player: {}'.format(self.marker2player))

    def prompt_move(self):
        if self.cur_player.is_real:
            msg = 'Enter move coordinate ({}): '
            msg = msg.format(self.board.CellLocation.COORDINATE_FORMAT)
            data = {
                NotificationKey.MESSAGE: msg,
                NotificationKey.MARKER: self.cur_marker,
                NotificationKey.PLAYER: self.cur_player
            }
            self.notify_observers(NotificationType.PLAYER_MOVE, data)
        else:
            loc = self.cur_player.get_move()
            self.do_move(str(loc))

    def start(self):
        self.setup()
        self.prompt_move()

    def get_result_msg(self):
        if self.ongoing:
            raise ValueError('Game is still ongoing!')
        if self.winner is None:
            msg = 'Draw game.'
        else:
            msg = '{!s} ({!r}) has won.'
            msg = msg.format(self.winner.name, self.winner.marker)
        return msg

    def end_board(self):
        data = { NotificationKey.MESSAGE: self.get_result_msg() }
        self.notify_observers(NotificationType.MESSAGE, data)
        # notify end game
        self.notify_observers(NotificationType.STATE, {})

    def do_move(self, loc_str):
        if not self.ongoing:
            raise ValueError('Game not ongoing!')

        # check valid move
        loc = None
        try:
            self.logger.info('Parsing loc: {}'.format(loc_str))
            loc = self.board.CellLocation.parse(loc_str)
        except:
            self.logger.error('Parse location error: {}'.format(loc_str))
            # prompt move again
            self.prompt_move()
            return 

        if not self.board.is_cell_empty(loc):
            self.prompt_move()
            return

        self.board.mark_cell(self.cur_marker, loc)
        if not self.cur_player.is_real:
            msg = '{} marked {!r} at {}'
            msg = msg.format(self.cur_player.name,
                             self.cur_player.marker,
                             loc)
            self.logger.info(msg)

        # increment marker
        n_markers = len(Marker)
        self.logger.debug('no. of markers: {}'.format(n_markers))
        self._marker = Marker((self._marker + 1) % n_markers)

        if not self.ongoing:
            self.end_board()
        else:
            self.prompt_move()

    def restart(self):
        self._marker = Marker.CIRCLE
        self.board.restart()


class GameBasic(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score = {marker:0 for marker in Marker}
        self.total_round = 0

    @property
    def ongoing(self):
        is_board_ongoing = self.board.state == BoardState.ONGOING
        max_round = self.game_configs[GameParameter.N_ROUNDS]
        is_max_round = self.total_round == max_round
        max_score = self.game_configs[GameParameter.FIRST_TO]
        has_max_score = map(lambda s: s >= max_score, self.score.values())
        has_max_score = any(list(has_max_score))
        return is_board_ongoing and not is_max_round and not has_max_score

    @property
    def winner(self):
        winner = None
        max_round = self.game_configs[GameParameter.N_ROUNDS]
        reached_max_round = self.total_round == max_round
        if not reached_max_round:
            return winner

        score_list = np.asarray(list(self.score.values()))
        draw = (score_list == score_list[0]).all()
        if not draw:
            max_score = -1
            for marker, player in self.marker2player.items():
                score = self.score[marker]
                winner = player if score > max_score else winner
                max_score = score if score > max_score else max_score

        return winner

    def get_result_msg(self):
        if self.winner is None:
            msg = 'Draw game after {} games.'.format(self.total_round)
        else:
            msg = '{!s} ({!r}) has won {} rounds out of {} games.'
            msg = msg.format(self.winner.name, 
                             self.winner.marker,
                             self.score[self.winner.marker],
                             self.total_round)
        return msg

    def get_round_msg(self, marker):
        msg = '{} ({!r}) wins round {}'
        round_winner = self.marker2player[marker]
        msg = msg.format(round_winner, marker, self.total_round - 1)
        return msg

    def end_board(self):
        self.total_round += 1
        marker_int = self.board.state - BoardState.CIRCLE_WIN
        if marker_int >= 0:
            marker = Marker(marker_int)
            self.score[marker] += 1
            reached_first_to = self.score[marker] >= self.game_configs[GameParameter.FIRST_TO]
            msg = self.get_result_msg() if reached_first_to else self.get_round_msg(marker)
        else:
            msg = 'Draw round {}'.format(self.total_round - 1)

        data = { NotificationKey.MESSAGE: msg }
        self.notify_observers(NotificationType.MESSAGE, data)

        reached_max_rounds = self.total_round >= self.game_configs[GameParameter.N_ROUNDS]
        if not reached_max_rounds:
            # game not finished yet, restart board
            self.board.restart()
            self.prompt_move()
        else:
            self.notify_observers(NotificationType.STATE, {})

    def restart(self):
        super().restart()
        self.score = {marker:0 for marker in Marker}
        self.total_round = 0
