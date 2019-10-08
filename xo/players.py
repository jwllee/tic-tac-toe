import random

from django.utils.module_loading import import_string
from . import minimax, mcts


def get_player(player_type):
    cls = import_string(player_type)
    return cls()


class RandomPlayer:
    def __repr__(self):
        RandomPlayer.__name__

    def play(self, game):
        empty_indexes = game.empty_indexes
        if not empty_indexes:
            return
        return random.choice(empty_indexes)


class MinimaxPlayer:
    def __repr__(self):
        return MinimaxPlayer.__name__

    def play(self, game):
        empty_indexes = game.empty_indexes
        if not empty_indexes:
            return
        return minimax.get_best_move(game)


class MCTSPlayer:
    def __repr__(self):
        return MCTSPlayer.__name__

    def play(self, game):
        empty_indexes = game.empty_indexes
        if not empty_indexes:
            return
        return mcts.get_best_move(game)
