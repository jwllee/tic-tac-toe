from collections import namedtuple
from abc import ABC, abstractmethod
from enum import Enum
import petname

from xo import utils


LOGGER = utils.make_logger(__file__)


__all__ = [
    'PlayerType',
    'PlayerReal',
    'PlayerAI'
]


class PlayerType(Enum):
    REAL = 1
    AI = 2


class Player(ABC):
    def __init__(self, player_type, name=None):
        utils.assert_isinstance('player_type', PlayerType, player_type)
        self.board = None
        self.marker = None
        self.player_type = player_type
        self.name = petname.generate() if name is None else name

    @property
    def is_real(self):
        return self.player_type == PlayerType.REAL

    @is_real.setter
    def is_real(self):
        raise NotImplementedError('Cannot set if player is real!')

    def save_data(self):
        pass


class PlayerReal(Player):
    def __init__(self, name=None):
        super().__init__(PlayerType.REAL, name=name)

    def get_move(self):
        raise NotImplementedError('Real player does not have get_move logic!')


class PlayerAI(Player):
    def __init__(self, strategy, name=None):
        super().__init__(PlayerType.AI, name=name)
        self.strategy = strategy

    def get_move(self):
        assert self.marker is not None, 'Player does not have marker!'
        assert self.strategy is not None, 'AI player does not have a strategy!'
        assert self.board is not None, 'Player does not have access to board!'
        return self.strategy.get_move(self.board, self.marker)

    def save_data(self):
        self.strategy.save_data()
