from enum import IntEnum
import sys, argparse


from xo.board.utils import *
from xo.utils import *
from xo.view import *
from xo.game import *
from xo.player import *
from xo.strategy import *


logger = make_logger(__file__)


class MainMenuOption(IntEnum):
    def __str__(self):
        return self.name

    NEW_GAME = 1
    EXIT = 2


class NewGameOption(IntEnum):
    def __str__(self):
        return self.name

    BASIC = 1


class EndGameOption(IntEnum):
    def __str__(self):
        return self.name

    AGAIN = 1
    MAIN_MENU = 2


class MainWindow:
    def __init__(self):
        self.logger = make_logger(MainWindow.__name__)


class TUIMainWindow(MainWindow):
    def __init__(self):
        self.view = TextView(TextBoard2dDisplayer())
        self.game = None

    def new_game(self):
        option = self.view.get_choice_input(NewGameOption, 'New game')

        if option == NewGameOption.BASIC:
            players = [
                PlayerReal(),
                PlayerAI(MinimaxStrategy(prune=True, cache=True))
            ]
            n_rows, n_cols, n_connects = 3, 3, 3
            board = Board2d(n_rows, n_cols, n_connects)
            self.game = Game(board, players)
            self.game.register_observer(self)
            self.game.start()

    def end_game(self):
        option = self.view.get_choice_input(EndGameOption, name='End game')
        if option == EndGameOption.AGAIN:
            self.new_game()
        elif option == EndGameOption.MAIN_MENU:
            self.show_main_menu()

    def update(self, type_, data):
        if type_ == NotificationType.PROMPT_MOVE:
            msg = data[NotificationKey.MESSAGE]
            loc_str = self.view.get_input(msg)
            self.game.do_move(loc_str)
        elif type_ == NotificationType.BOARD_UPDATE:
            board = data[NotificationKey.BOARD]
            self.view.board_displayer.display(board)
        elif type_ == NotificationType.GAME_END:
            self.end_game()

    def show_main_menu(self):
        option = self.view.get_choice_input(MainMenuOption, name='Main menu')
        if option == MainMenuOption.EXIT:
            exit()
        elif option == MainMenuOption.NEW_GAME:
            self.new_game()

    def start(self):
        msg = 'Welcome to Tic Tac Toe'
        self.view.display_msg(msg)
        self.show_main_menu()


def run_terminal_mode():
    logger.info('Running terminal mode...')
    main_window = TUIMainWindow()
    main_window.start()


if __name__ == '__main__':
    run_terminal_mode()
