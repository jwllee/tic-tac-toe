import random

from django.utils.module_loading import import_string
from . import minimax


def get_player(player_type):
    cls = import_string(player_type)
    return cls()


class RandomPlayer:
    def play(self, game):
        empty_indexes = game.empty_indexes
        if not empty_indexes:
            return
        return random.choice(empty_indexes)


class MinimaxPlayer:
    def play(self, game):
        empty_indexes = game.empty_indexes
        if not empty_indexes:
            return
        return minimax.get_best_move(game)
