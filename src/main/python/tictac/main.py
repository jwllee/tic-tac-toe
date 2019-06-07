from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
from tictac import utils
from tictac.game import *
from tictac.player import *
from tictac.strategy import *
from tictac.view import *

import sys, argparse


logger = utils.make_logger(utils.LoggerType.DEFAULT.name)


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
    # @todo: make a factory for games
    players = [
        PlayerReal(),
        PlayerAI(RandomStrategy())
    ]
    game_configs = {
        GameParameter.BOARD_DIM: 5,
        GameParameter.FIRST_TO: 3,
        GameParameter.N_ROUNDS: 5
    }
    displayer = TextBoard2dDisplayer()
    view = TextView(displayer)
    game = GameBasic(players, game_configs, view)
    game.start()


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

    

