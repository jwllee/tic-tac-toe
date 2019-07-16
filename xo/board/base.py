from abc import ABC, abstractmethod, abstractclassmethod
import numpy as np
from xo import utils
from xo.board.utils import *


__all__ = [
    'AbstractBoard'
]


class AbstractBoard(ABC):
    def __init__(self):
        self._state = BoardState.ONGOING
        self.observers = list()
        self.logger = utils.make_logger(AbstractBoard.__name__)

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
    def state(self):
        return self._state

    @property
    def n_cells(self):
        raise NotImplementedError('Please implement this method.')

    @property
    def has_winner(self):
        raise NotImplementedError('Please implement this method.')

    #------------------------------------------------------------ 
    # Abstract methods
    #------------------------------------------------------------ 
    @abstractmethod
    def copy(self, include_observers=False):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def __hash__(self):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def restart(self):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def is_cell_empty(self, loc):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def get_cell(self, loc):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def get_empty_cells(self):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def get_filled_cells(self):
        raise NotImplementedError('Please implement this method.')

    @property
    def full(self):
        raise NotImplementedError('Please implement this method.')

    @property
    def empty(self):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def mark_cell(self, marker, loc):
        raise NotImplementedError('Please implement this method.') 

    @abstractmethod
    def unmark_cell(self, marker, loc):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def is_winner(self, marker):
        raise NotImplementedError('Please implement this method.')
