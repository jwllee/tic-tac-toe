from . import utils
from abc import ABC, abstractmethod
import sys


__all__ = [
    'TextBoard2dDisplayer',
    'TextView'
]


class View(ABC):
    def __init__(self, board_displayer):
        self.board_displayer = board_displayer
        self.logger = utils.make_logger(View.__name__)

    @abstractmethod
    def update(self, board):
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


class TextBoard2dDisplayer:
    EMPTY = '_'

    def display(self, board, f=sys.stdout):
        print('Board', file=f)
        for row in range(board.n_rows):
            s = ''
            for col in range(board.n_cols):
                loc_str = '{}, {}'.format(row, col)
                loc = board.CellLocation.parse(loc_str)
                if board.is_cell_empty(loc):
                    s += str(self.EMPTY)
                else:
                    cell = board.get_cell(loc)
                    s += repr(cell.content)
            print(s, file=f)


class TextView(View):
    def update(self, board):
        self.logger.debug('Updating view...')
        self.board_displayer.display(board)

    def get_input(self, msg=None):
        if msg is not None:
            s = input(msg)
        else:
            s = input()
        return s

    def display_msg(self, msg):
        print(msg)

    def get_choice_input(self, choices, msg=''):
        msg = 'Enter choice:'
        self.display_msg(msg)

        while True:
            for i, c in enumerate(choices):
                msg = '{}: {}'.format(i, str(c))
                self.display_msg(msg)

            line = sys.stdin.rstrip()
            try:
                i = int(line)
                if i in range(len(choices)):
                    return list(choices)[i]
            except:
                err_msg = 'Invalid choice input: {}'.format(line)
                self.logger.debug(err_msg)
                self.display_msg(err_msg)

            msg = 'Re-enter choice:'
            self.display_msg(msg)
