from enum import Enum
from abc import ABC, abstractmethod
from . import board as board_mod
from . import player as player_mod
from . import utils


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
        self.logger = utils.make_logger(self.__class__.__name__)
        self.players = players
        self.marker2player = dict()
        self.game_configs = game_configs
        self.board = None
        self.view = view
        self.__marker = board_mod.Marker.CIRCLE

    #------------------------------------------------------------ 
    # Properties
    #------------------------------------------------------------ 
    @property
    def state(self):
        return self.board.state

    @state.setter
    def state(self, s):
        raise NotImplementedError('Cannot set current state!')

    @property
    def marker(self):
        return self.__marker

    @marker.setter
    def marker(self, m):
        raise NotImplementedError('Cannot set current marker!')

    #------------------------------------------------------------ 
    # Abstract methods
    #------------------------------------------------------------ 
    @abstractmethod
    def update_board(self, move):
        raise NotImplementedError('Please implement this method.')

    def end(self):
        if self.state == board_mod.BoardState.DRAW:
            msg = 'Draw game.'
        else:
            marker = self.state - board_mod.BoardState.CIRCLE_WIN
            msg = '{} has won.'.format(marker)
        self.view.display_msg(msg)

    def setup(self):
        for marker, player in zip(board_mod.Marker, self.players):
            player.board = self.board
            player.marker = marker
            self.marker2player[marker] = player

    def start(self):
        self.setup()

        while self.state == board_mod.BoardState.ONGOING:
            self.logger.debug('Next round...')
            cur_player = self.marker2player[self.__current_marker]

            if isinstance(cur_player, player_mod.PlayerReal):
                move = self.prompt_move()
            else:
                move = cur_player.get_move()

            self.update_board(move)

            # increment marker
            self.__marker += 1
            self.__marker %= len(board_mode.Marker)

        self.end()

    def prompt_move(self):
        msg = 'Enter move coordinate ({})'
        msg = msg.format(self.board.coordinate_format)
        move = None
        while not self.board.is_move_valid(move):
            move = self.view.get_input(msg)
        return move


class GameBasic(Game):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self):
        n_rows = self.game_configs[GameParameter.BOARD_DIM]
        n_cols = self.game_configs[GameParameter.BOARD_DIM]
        self.board = board_mod.Board2d(n_rows, n_cols)
        super().setup()

    def mark_cell(self, marker, loc):
        is_marked = self.board.mark_cell(marker, loc)
        return is_marked
