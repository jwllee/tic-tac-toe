import time
import numpy as np
from collections import namedtuple
from . import board_utils
from . import models


field_names = [
    'n_rows',
    'n_cols',
    'n_connects',
    'board_x',
    'board_o',
]
State = namedtuple('State', field_names)


def get_max_score(n_rows, n_cols):
    return n_rows * n_cols


def get_utility(state, max_score):
    utility = 0
    winner = board_utils.is_game_over(
        state.board_x,
        state.board_o,
        state.n_rows,
        state.n_cols,
        state.n_connects
    )
    if winner == board_utils.MARKER_X:
        utility = max_score
    elif winner == board_utils.MARKER_O:
        utility = -max_score
    return utility


def add_cross(board, index):
    flag = 1 << index
    return board | flag


def add_circle(board, index):
    flag = 1 << index
    return board | flag


def mark_cell(state, marker, index):
    is_x = marker == board_utils.MARKER_X
    is_o = marker == board_utils.MARKER_O
    if not (is_x or is_o):
        err_msg = 'Do not recognize marker {}'.format(marker)
        raise ValueError(err_msg)
    if is_x:
        board_x = add_cross(state.board_x, index)
        board_o = state.board_o
    else:
        board_o = add_circle(state.board_o, index)
        board_x = state.board_x
    new_state = State(
        state.n_rows,
        state.n_cols,
        state.n_connects,
        board_x,
        board_o,
    )
    return new_state


def get_empty_indexes(state):
    n_cells = state.n_rows * state.n_cols
    empty_indexes = board_utils.get_empty_indexes(state.board_x, 
                                                  state.board_o,
                                                  n_cells)
    return empty_indexes


def get_best_move(game):
    start = time.time()
    state = State(
        game.n_rows, game.n_cols, game.n_connects,
        game.board_x, game.board_o
    )

    eval_marker = board_utils.get_next_player(game.board_x, game.board_o, game.n_cells)
    color = 1 if eval_marker == board_utils.MARKER_X else -1
    alpha = -np.inf
    beta = np.inf
    depth_limit = 10

    info_msg = 'Getting best move for Player {} at {} with depth limit {}'
    info_msg = info_msg.format(eval_marker, game, depth_limit)
    print(info_msg)

    utility, best_move = get_negamax(state, eval_marker, depth_limit, alpha, beta, color)

    end = time.time()
    took = end - start

    # update the cache for state
    # save_cache(state, best_score, True)

    info_msg = 'Took {:.3f}s to compute minimax value'
    info_msg = info_msg.format(took)
    print(info_msg)

    state_utility = color * utility
    info_msg = 'Minimax move for Player {} is index {} with value {}'
    info_msg = info_msg.format(eval_marker, best_move, state_utility)
    print(info_msg)

    return best_move


def is_game_over(state):
    is_over = board_utils.is_game_over(
        state.board_x, 
        state.board_o,
        state.n_rows,
        state.n_cols,
        state.n_connects
    )
    return is_over


def save_cache(state, utility, is_exact):
    models.BoardState.cache(
        state.board_x,
        state.board_o,
        state.n_rows,
        state.n_cols,
        state.n_connects,
        utility,
        is_exact,
    )


def get_cache(state):
    result = models.BoardState.get_cache(
        state.board_x,
        state.board_o,
        state.n_rows,
        state.n_cols,
        state.n_connects,
    )
    return result


def get_negamax(state, marker, depth, alpha, beta, color):
    max_score = get_max_score(state.n_rows, state.n_cols)

    if depth == 0 or is_game_over(state):
        return color * get_utility(state, max_score), None

    empty_indexes = get_empty_indexes(state)
    best_score = -np.inf
    best_index = None

    for index in empty_indexes:
        child = mark_cell(state, marker, index)
        next_marker = board_utils.get_opposite_marker(marker)
        child_value, _ = get_negamax(child, next_marker, depth - 1, -beta, -alpha, -color)
        child_value = -child_value
        
        if child_value > best_score:
            best_score = child_value
            best_index = index

        alpha = max(alpha, best_score)
        if alpha >= beta:
            break

    return best_score, best_index
