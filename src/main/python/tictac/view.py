from . import utils
from abc import ABC, abstractmethod
import sys
from PyQt5.QtWidgets import (QGridLayout, QPushButton, QWidget, QSizePolicy)
from functools import partial

from utils import NotificationKey, NotificationType


__all__ = [
    'TextBoard2dDisplayer',
    'TextView', 
    'GUIBoard2dDisplayer',
    'GUIBoard2dButton',
    'GUIBoard2dWidget'
]


class View(ABC):
    def __init__(self, board_displayer):
        self.board_displayer = board_displayer
        self.logger = utils.make_logger(View.__name__)

    @abstractmethod
    def update(self, _type, data):
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
        self.logger = utils.make_logger(Displayer.__name__)

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
                loc = board.CellLocation.parse(loc_str)
                if board.is_cell_empty(loc):
                    s += str(self.EMPTY) + ' '
                else:
                    cell = board.get_cell(loc)
                    s += repr(cell.content) + ' '
            print(s, file=where)


class TextView(View):
    def update(self, _type, data):
        self.logger.debug('Updating view...')
        board = data[NotificationKey.STATE]
        self.board_displayer.display(board)

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


class GUIBoard2dButton(QPushButton):
    WIDTH = 100
    HEIGHT = 100

    def __init__(self, text, width, height, parent=None):
        super().__init__(parent)
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)
        self.setText(text)
        self.setFixedSize(width, height)


class GUIBoard2dWidget(QWidget):
    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        policy.setHeightForWidth(True)
        self.setSizePolicy(policy)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setFixedSize(width, height)


class GUIBoard2dDisplayer(Displayer):
    def __init__(self, on_clicked, button_attrib):
        self.on_clicked = on_clicked
        self.button_attrib = button_attrib

    def make_button(self, text, row, col):
        width = self.button_attrib['width']
        height = self.button_attrib['height']
        button = GUIBoard2dButton(text, GUIBoard2dButton.WIDTH, 
                                  GUIBoard2dButton.HEIGHT)
        on_clicked = partial(self.on_clicked, 
                             button, row, col)
        button.clicked.connect(on_clicked)
        # set attributes
        return button
    
    def display(self, board, where):
        for row in range(board.n_rows):
            for col in range(board.n_cols):
                loc_str = '{}, {}'.format(row, col)
                loc = board.CellLocation.parse(loc_str)
                if board.is_cell_empty(loc):
                    button_text = str(self.EMPTY)
                else:
                    cell = board.get_cell(loc)
                    button_text = repr(cell.content)
                button = self.make_button(button_text, row, col)
                where.layout.addWidget(button, row, col)
