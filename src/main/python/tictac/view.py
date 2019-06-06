from . import utils
from abc import ABC, abstractmethod
import sys


class View(ABC):
    def __init__(self, board_view):
        self.board_view = board_view
        self.logger = utils.make_logger(self.__class__.__name__)

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


class Terminal2dBoard:
    EMPTY = '_'

    def display(self, board):
        for row in range(board.n_rows):
            s = ''
            for col in range(board.n_cols):
                if board.is_cell_empty(row, col):
                    s.append(EMPTY)
                else:
                    cell = board.get_cell(row, col)
                    s.append(cell.val.marker)
            print(s)


class TerminalView(View):
    def update(self, board):
        self.board_view.display(board)

    def get_input(self, msg=None):
        if msg is not None:
            self.display_msg(msg)
        return sys.stdin.rstrip()

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