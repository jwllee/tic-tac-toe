import pickle, os
from xo.utils import *

from . import base
from . import minimax
from . import utils

from .base import *
from .minimax import *


class StrategyFactory:
    def __init__(self, game_cache_dir):
        self.game_cache_dir = game_cache_dir
        self.logger = make_logger(StrategyFactory.__name__)

    def new_minimax_strategy(self, n_rows, n_cols, n_connects, 
                             prune=True, cache=True):
        table_fname = '{}-{}-{}.pickle'
        table_fname = table_fname.format(n_rows, n_cols, n_connects)
        minimax_dir = os.path.join(self.game_cache_dir, 'minimax')
        if not os.path.isdir(minimax_dir):
            os.mkdir(minimax_dir)

        table_fp = os.path.join(minimax_dir, table_fname)

        table = dict()
        if os.path.exists(table_fp) and os.path.isfile(table_fp):
            self.logger.info('Loading transposition table')
            with open(table_fp, 'rb') as f:
                table = pickle.load(f)

        self.logger.debug('Table: {}'.format(table))
        strategy = MinimaxStrategy(table_fp, prune=prune,
                                   cache=cache, table=table)
        return strategy


