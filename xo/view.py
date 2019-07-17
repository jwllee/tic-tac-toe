from abc import ABC, abstractmethod
import sys
from functools import partial

from xo.board.utils import *
from xo.utils import *
from xo.board import *


__all__ = [
    'TextBoard2dDisplayer',
    'TextView', 
]


class View(ABC):
    def __init__(self, board_displayer):
        self.board_displayer = board_displayer
        self.logger = make_logger(View.__name__)

    @abstractmethod
    def update(self, type_, data):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def get_input(self, msg=''):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def display_msg(self, msg):
        raise NotImplementedError('Please implement this method.')

    @abstractmethod
    def get_choice_input(self, choices, msg=''):
        raise NotImplementedError('Please implement this method.')


class Displayer(ABC):
    EMPTY = '-'

    def __init__(self):
        self.logger = make_logger(Displayer.__name__)

    @abstractmethod
    def display(self, board, where):
        raise NotImplementedError('Please implement this method.')


class TextBoard2dDisplayer(Displayer):
    def display(self, board, where=sys.stdout):
        print('Board', file=where)
        for row in range(board.n_rows):
            s = ' '
            for col in range(board.n_cols):
                loc_str = '{}, {}'.format(row, col)
                loc = CellLocation2d.parse(loc_str)
                if board.is_cell_empty(loc):
                    s += str(self.EMPTY) + ' '
                else:
                    cell = board.get_cell(loc)
                    s += repr(cell.val) + ' '
            print(s, file=where)


class TextView(View):
    def update(self, type_, data):
        self.logger.debug('Updating view...')
        if type_ == NotificationType.PROMPT_MOVE:
            board = data[NotificationKey.BOARD]
            self.board_displayer.display(board)
        elif type_ == NotificationType.GAME_END:
            result_msg = data[NotificationKey.MESSAGE]
            self.display_msg(result_msg)

    def get_input(self, msg=None):
        if msg is not None:
            s = input(msg)
        else:
            s = input()
        return s

    def display_msg(self, msg):
        print(msg)

    def get_choice_input(self, choices, name=''):
        header = '------------------------------{}------------------------------'.format(name)
        self.display_msg(header)
        footer = '-' * len(header)

        while True:
            for i, c in enumerate(choices):
                msg = '{}. {}'.format(i + 1, str(c))
                self.display_msg(msg)
            self.display_msg(footer)

            line = self.get_input('Select: ')
            try:
                i = int(line) - 1
                if i in range(len(choices)):
                    return list(choices)[i]
            except:
                err_msg = 'Invalid choice input: {}'.format(line)
                self.logger.debug(err_msg)
                self.display_msg(err_msg)

            self.display_msg(header)
