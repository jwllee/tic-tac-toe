from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import QMainWindow, QWidget
from enum import IntEnum
from tictac import utils
from tictac.game import *
from tictac.player import *
from tictac.strategy import *
from tictac.view import *
from tictac.board import *

import sys, argparse


logger = utils.make_logger(utils.LoggerType.DEFAULT.name)


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
        self.logger = utils.make_logger(MainWindow.__name__)


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
            game_configs = {
                GameParameter.BOARD_DIM: 3,
                GameParameter.FIRST_TO: 3,
                GameParameter.N_ROUNDS: 5
            }
            n_rows = game_configs[GameParameter.BOARD_DIM]
            n_cols = n_rows
            board = Board2d(n_rows, n_cols)
            board.register_observer(self.view)
            self.game = GameBasic(board, players, game_configs)
            self.game.register_observer(self)
            self.game.start()

    def end_game(self):
        option = self.view.get_choice_input(EndGameOption, name='End game')
        if option == EndGameOption.AGAIN:
            self.new_game()
        elif option == EndGameOption.MAIN_MENU:
            self.show_main_menu()

    def update(self, type_, data):
        if type_ == utils.NotificationType.MESSAGE:
            msg = data[utils.NotificationKey.MESSAGE]
            self.view.display_msg(msg)
        elif type_ == utils.NotificationType.PLAYER_MOVE:
            msg = data[utils.NotificationKey.MESSAGE]
            loc_str = self.view.get_input(msg)
            self.game.do_move(loc_str)
        elif type_ == utils.NotificationType.STATE:
            if not self.game.ongoing:
                option = self.view.get_choice_input(EndGameOption, name='End game')

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

def run_gui_mode():
    logger.info('Running GUI mode...')
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = QMainWindow()
    n_rows, n_cols = 3, 3
    board = Board2d(n_rows, n_cols)

    def on_clicked(button, row, col):
        print('Button at ({}, {}) clicked'.format(row, col))
        button.setText('Clicked')

    width = n_rows * 110
    height = n_cols * 110
    attribs = {
        'width': 100,
        'height': 100
    }
    widget = GUIBoard2dWidget(width, height)
    window.setCentralWidget(widget)
    displayer = GUIBoard2dDisplayer(on_clicked, attribs)
    displayer.display(board, widget)
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)


def run_terminal_mode():
    logger.info('Running terminal mode...')
    main_window = TUIMainWindow()
    main_window.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store',
                        default=False, dest='run_terminal',
                        help='Whether to run game in terminal mode')

    args = parser.parse_args()

    if args.run_terminal:
        run_terminal_mode()
    else:
        run_gui_mode()

    

