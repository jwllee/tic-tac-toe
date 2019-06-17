from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
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


class TUIMainWindow:
    def __init__(self):
        self.view = TextView(TextBoard2dDisplayer())
        self.game = None

    def get_main_menu_options(self):
        options = [
            MainMenuOption.NEW_GAME, 
            MainMenuOption.EXIT
        ]
        return options

    def get_new_game_options(self):
        options = [
            NewGameOption.BASIC
        ]
        return options

    def new_game(self):
        options = self.get_new_game_options()
        option = self.view.get_choice_input(options, 'New game')

        if option == NewGameOption.BASIC:
            players = [
                PlayerReal(),
                PlayerAI(MinimaxStrategy())
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

    def update(self, _type, data):
        if _type == utils.NotificationType.MESSAGE:
            msg = data[utils.NotificationKey.MESSAGE]
            self.view.display_msg(msg)
        elif _type == utils.NotificationType.PLAYER_MOVE:
            msg = data[utils.NotificationKey.MESSAGE]
            loc_str = self.view.get_input(msg)
            self.game.do_move(loc_str)

    def do_option(self, option):
        if option == MainMenuOption.EXIT:
            exit()
        elif option == MainMenuOption.NEW_GAME:
            self.new_game()

    def start(self):
        msg = 'Welcome to Tic Tac Toe'
        self.view.display_msg(msg)

        options = self.get_main_menu_options()
        option = self.view.get_choice_input(options, 'Main menu')
        self.do_option(option)

def run_gui_mode():
    logger.info('Running GUI mode...')
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = QMainWindow()
    window.resize(250, 150)
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

    

