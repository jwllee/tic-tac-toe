import time, operator
import numpy as np
from collections import namedtuple
from . import board_utils, win_state_utils
from . import models
from .utils import timeit


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


def get_depth_bound(state):
    """Search depth cannot be more than the number of empty spaces.
    """
    empty_indexes = get_empty_indexes(state)
    return len(empty_indexes)


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
    # seconds
    remaining_time = 5
    # at least 3 steps ahead
    depth = 1
    depth_bound = get_depth_bound(state)

    info_msg = 'Getting best move for Player {} at {} within {} seconds'
    info_msg = info_msg.format(eval_marker, game, remaining_time)
    print(info_msg)

    it = 1
    while remaining_time > 0:
        info_msg = 'Iteration {}: depth: {}, depth bound: {} remaining time: {:.3f}s'
        info_msg = info_msg.format(it, depth, depth_bound, remaining_time)
        print(info_msg)

        utility, best_move, flag, remaining_time = get_negamax(
            state, eval_marker, depth, alpha, beta, color, True, remaining_time)

        if depth == depth_bound:
            break

        depth = 1 + depth if 1 + depth <= depth_bound else depth_bound
        it += 1

    end = time.time()
    took = end - start

    state_utility = color * utility
    flag_str = board_utils.flag2str(flag)
    info_msg = 'Minimax move for Player {} is index {} with "{}" value {} at depth {} with remaining time: {:.3f}s'
    info_msg = info_msg.format(eval_marker, best_move, flag_str, state_utility, depth, remaining_time)
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


def save_cache(state, depth, utility, flag):
    # make sure depth is valid 
    depth = depth if depth < 1 << 31 else 1 << 31
    models.BoardState.cache(
        state.board_x,
        state.board_o,
        state.n_rows,
        state.n_cols,
        state.n_connects,
        depth,
        utility,
        flag
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


def get_heuristic(state, max_score):
    win_board = win_state_utils.get_board_wins(state.n_rows, state.n_cols, state.n_connects)
    n_wins = len(win_board)

    # measure its closeness to winning to all the wins
    # basically infinity
    max_score = -(1 << 30)
    n_cells = state.n_rows * state.n_cols
    marker = board_utils.get_next_player(state.board_x, state.board_o, n_cells)

    if marker == board_utils.MARKER_X:
        board = state.board_x
        board_oppo = state.board_o
    else:
        board = state.board_o
        board_oppo = state.board_x

    for win in win_board:
        # first check if the win is possible to reach
        # should equal 0 since where there's 1 in win state, it should be empty in opposition board
        is_valid = (win & board_oppo) == 0
        if not is_valid:
            continue

        same = board & win
        score = bin(same).count('1') 
        max_score = max(score, max_score)

    max_score = max_score if marker == board_utils.MARKER_X else -max_score

    return max_score


def sort_empty_indexes(state, marker, empty_indexes):
    to_sort = list()
    unknown = list()
    max_score = get_max_score(state.n_rows, state.n_cols)

    for index in empty_indexes:
        child = mark_cell(state, marker, index)
        cache = get_cache(child)
        if cache:
            to_sort.append((index, cache.value, cache.flag))
        else:
            # use heuristic
            heuristic = get_heuristic(child, max_score)
            to_sort.append((index, heuristic, board_utils.HEURISTIC))

    reverse = True if marker == board_utils.MARKER_X else False
    flag_key = lambda tuple_: tuple_[2]
    value_key = lambda tuple_: tuple_[1]
    to_sort = sorted(to_sort, key=flag_key)
    to_sort = sorted(to_sort, key=value_key, reverse=reverse)
    results = list(map(lambda t: t[0], to_sort))
    return results


def get_negamax(state, marker, depth, alpha, beta, color, is_root, remaining_time):
    time_start = time.time()
    flag = board_utils.EXACT
    max_score = get_max_score(state.n_rows, state.n_cols)
    alpha_orig = alpha

    if not is_root:
        cache = get_cache(state)

        if cache and cache.depth >= depth:
            if cache.flag == board_utils.EXACT:
                return cache.value, None, flag, remaining_time
            elif cache.flag == board_utils.LOWER:
                alpha = max(alpha, cache.value)
            elif cache.flag == board_utils.UPPER:
                beta = min(beta, cache.value)

        if alpha >= beta:
            return cache.value, None, flag, remaining_time

    if is_game_over(state):
        return color * get_utility(state, max_score), None, flag, remaining_time

    if depth == 0:
        flag = board_utils.HEURISTIC
        return color * get_heuristic(state, max_score), None, flag, remaining_time

    empty_indexes = get_empty_indexes(state)
    empty_indexes = sort_empty_indexes(state, marker, empty_indexes)
    
    best_score = -np.inf
    best_index = None

    for index in empty_indexes:
        child = mark_cell(state, marker, index)
        next_marker = board_utils.get_opposite_marker(marker)
        child_result = get_negamax(
            child, next_marker, depth - 1, -beta, -alpha, -color, False, remaining_time)
        child_value = -child_result[0]
        child_flag = child_result[2]
        flag = child_flag if child_flag == board_utils.HEURISTIC else flag
        
        if child_value > best_score:
            best_score = child_value
            best_index = index

        alpha = max(alpha, best_score)
        if alpha >= beta:
            break

        time_check = time.time()
        took = time_check - time_start
        if took >= remaining_time:
            break

    if best_score <= alpha_orig:
        flag = board_utils.UPPER
    elif best_score >= beta:
        flag = board_utils.LOWER
    else:
        flag = board_utils.EXACT

    # only save non-heuristic values
    save_cache(state, depth, best_score, flag)

    # update time
    time_check = time.time()
    took = time_check - time_start
    remaining_time -= took

    return best_score, best_index, flag, remaining_time
