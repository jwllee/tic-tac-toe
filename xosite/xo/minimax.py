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
    'depth',
    'is_max',
]
State = namedtuple('State', field_names)


def get_max_score(n_rows, n_cols):
    return n_rows * n_cols


def get_utility(state, marker, max_score):
    utility = 0
    winner = board_utils.is_game_over(
        state.board_x,
        state.board_o,
        state.n_rows,
        state.n_cols,
        state.n_connects
    )
    if winner == marker:
        utility = max_score - state.depth
    elif winner is not None:
        utility = -(max_score - state.depth)
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
        state.depth + 1,
        not state.is_max
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
    eval_marker = board_utils.get_next_player(game.board_x, game.board_o, game.n_cells)
    next_marker = board_utils.get_opposite_marker(eval_marker)
    state = State(
        game.n_rows, game.n_cols, game.n_connects,
        game.board_x, game.board_o, 0, True
    )
    empty_indexes = board_utils.get_empty_indexes(game.board_x, game.board_o, game.n_cells)

    best_score = -np.inf
    best_move = None

    info_msg = 'Getting best move for Player {} at {}'
    info_msg = info_msg.format(eval_marker, game)
    print(info_msg)

    for index in empty_indexes:
        child = mark_cell(state, eval_marker, index)
        value = get_minimax(index, child, next_marker, eval_marker)
        if value > best_score:
            best_score = value
            best_move = index

    end = time.time()
    took = end - start

    # update the cache for state
    save_cache(state, best_score)

    info_msg = 'Took {:.3f}s to compute minimax value'
    info_msg = info_msg.format(took)
    print(info_msg)

    info_msg = 'Minimax move for Player {} is index {}'
    info_msg = info_msg.format(eval_marker, best_move)
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


def save_cache(state, utility):
    models.BoardState.cache(
        state.board_x,
        state.board_o,
        state.n_rows,
        state.n_cols,
        state.n_connects,
        state.is_max,
        state.depth,
        utility
    )


def get_cache(state):
    result = models.BoardState.get_cache(
        state.board_x,
        state.board_o,
        state.n_rows,
        state.n_cols,
        state.n_connects,
        state.is_max,
        state.depth,
    )
    return result
    # return None


def is_pruneable(node_stack, minimax, is_max):
    pruneable = False
    if len(node_stack) > 1:
        parent = node_stack[-2]
        minimax_parent = parent[4]
        lower_larger_than_par_upper = is_max and minimax[0] > minimax_parent[1]
        upper_less_than_par_lower = not is_max and minimax[1] < minimax_parent[0]

        if lower_larger_than_par_upper or upper_less_than_par_lower:
            pruneable = True
    return pruneable


def get_minimax(index, state, cur_marker, eval_marker):
    info_msg = 'Computing minimax value for Player {} at {}'
    info_msg = info_msg.format(cur_marker, state)
    print(info_msg)
    max_score = get_max_score(state.n_rows, state.n_cols)
    
    if is_game_over(state):
        return get_utility(state, eval_marker, max_score)

    empty_indexes = get_empty_indexes(state)
    is_max = cur_marker == eval_marker
    minimax = [-np.inf, np.inf]
    node_stack = [(
        state,          # state
        index,          # move that got to this state
        eval_marker,    # marker for move
        empty_indexes,
        minimax,        # minimax values
        cur_marker
    )]

    while node_stack:
        state, last_move, last_marker, children, minimax, cur_marker = node_stack[-1]

        try:
            index = children.pop(0)
            is_max = last_marker == eval_marker

            if is_pruneable(node_stack, minimax, is_max):
                continue

            child_state = mark_cell(state, cur_marker, index)

            # check if we have already seen this state
            cache = get_cache(child_state)

            if cache:
                # cache value is stored assuming that it was a max layer
                utility_child = cache.value 
                minimax_child = [utility_child, utility_child]
                empty_indexes_child = []
            else:
                minimax_child = [-np.inf, np.inf]
                empty_indexes_child = get_empty_indexes(child_state)
            # minimax_child = [-np.inf, np.inf]
            # empty_indexes_child = get_empty_indexes(child_state)

            next_marker = board_utils.get_opposite_marker(cur_marker)
            node = (
                child_state,
                index,
                cur_marker,
                empty_indexes_child,
                minimax_child,
                next_marker
            )
            node_stack.append(node)
        except IndexError:
            if is_game_over(state):
                utility = get_utility(state, eval_marker, max_score)
            else:
                utility = minimax[1] if state.is_max else minimax[0]
                # update cache
                save_cache(state, utility)

            node_stack.pop(-1)
            if node_stack:
                is_max = last_marker == eval_marker
                parent = node_stack[-1]
                empty_indexes_parent = parent[3]
                minimax_parent = parent[4]
                if is_max:
                    minimax_parent[0] = max(minimax_parent[0], utility)
                    if len(empty_indexes_parent) == 0:
                        minimax_parent[1] = max(utility, minimax_parent[0])
                else:
                    minimax_parent[1] = min(minimax_parent[1], utility)
                    if len(empty_indexes_parent) == 0:
                        minimax_parent[0] = min(utility, minimax_parent[1])
            else:
                # computed minimax value
                return utility
