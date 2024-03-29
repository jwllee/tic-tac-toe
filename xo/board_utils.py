import numpy as np
from xo import win_state_utils
from collections import namedtuple


field_names = [
    'row_ind',
    'col_ind',
    'marker'
]
Move = namedtuple('Move', field_names)


MARKER_X = 'X'
MARKER_O = 'O'
EXACT = 0
LOWER = 1
UPPER = 2
HEURISTIC = 3


def flag2str(flag):
    d = {
        EXACT: 'exact',
        LOWER: 'lower',
        UPPER: 'upper',
        HEURISTIC: 'heuristic',
    }
    return d[flag]


def get_empty_indexes(board_x, board_o, n_cells):
    indexes = []
    for i in range(n_cells):
        flag = 1 << i
        has_x = board_x & flag
        has_o = board_o & flag
        if not (has_x or has_o):
            indexes.append(i)
    return indexes


def get_board_str(board_x, board_o, n_cells):
    s = ''
    for i in range(n_cells):
        v = ' '
        flag = 1 << i
        has_x = board_x & flag
        has_o = board_o & flag
        if has_x:
            v = MARKER_X
        if has_o:
            v = MARKER_O
        s += v
    return s


def get_board_mat(board_x, board_o, n_rows, n_cols):
    n_cells = n_rows * n_cols
    mat = np.empty(n_cells, dtype=np.str)
    for i in range(n_cells):
        v = ' '
        flag = 1 << i
        has_x = board_x & flag
        has_o = board_o & flag
        if has_x:
            v = MARKER_X
        if has_o:
            v = MARKER_O
        mat[i] = v
    mat = mat.reshape((n_rows, n_cols))
    return mat


def get_opposite_marker(marker):
    is_cross = marker == MARKER_X
    is_circle = marker == MARKER_O
    err_msg = 'Do not recognize marker: {}'
    err_msg = err_msg.format(marker)
    assert is_cross or is_circle, err_msg
    return MARKER_O if is_cross else MARKER_X


def get_next_player(board_x, board_o, n_cells):
    n_x = 0
    n_o = 0
    for i in range(n_cells):
        n_x += board_x & 0b1
        n_o += board_o & 0b1
        board_x >>= 1
        board_o >>= 1

    err_msg = 'Board has {} X and {} O'
    err_msg = err_msg.format(n_x, n_o)
    assert abs(n_x - n_o) == 1 or n_x == n_o, err_msg
    player = MARKER_O if n_o < n_x else MARKER_X
    return player


def get_cur_player(board_x, board_o, n_cells):
    next_player = get_next_player(board_x, board_o, n_cells)
    if next_player == MARKER_O:
        player = MARKER_X
    else:
        player = MARKER_O
    return player


def is_filled(board_x, board_o, full_state):
    current_state = board_o | board_x
    filled = (current_state & full_state) == full_state
    return filled


def is_game_over(board_x, board_o, n_rows, n_cols, n_connects):
    # check for drawn first
    board_win = win_state_utils.get_board_wins(n_rows, n_cols, n_connects)
    # None for ongoing
    result = None
    for win in board_win:
        x_win = (board_x & win) == win
        o_win = (board_o & win) == win
        if x_win:
            result = 'X'
            break
        elif o_win:
            result = 'O'
            break
    n_cells = n_rows * n_cols
    full_state = (1 << n_cells) - 1
    filled = is_filled(board_x, board_o, full_state)
    if result is None and filled:
        result = ' '
    return result


def is_empty(board_x, board_o, index):
    flag = 1 << index
    has_x = board_x & flag
    has_o = board_o & flag
    return (has_x | has_o) == 0


def reflect_y(board, n_rows, n_cols):
    n_cells = n_rows * n_cols
    reflected = 0

    for ind in range(n_cells):
        row_ind = ind // n_cols
        col_ind = ind % n_cols
        col_ind_r = n_cols - (col_ind + 1)
        ind_r = row_ind * n_cols + col_ind_r

        flag = 1 << ind
        flag_r = 1 << ind_r
        if (board & flag) == flag:
            reflected |= flag_r

    return reflected


def reflect_x(board, n_rows, n_cols):
    n_cells = n_rows * n_cols
    reflected = 0

    for ind in range(n_cells):
        row_ind = ind // n_cols
        col_ind = ind % n_cols

        # same column but different row
        row_ind_r = n_rows - (row_ind + 1)
        ind_r = row_ind_r * n_cols + col_ind

        flag = 1 << ind
        flag_r = 1 << ind_r
        if (board & flag) == flag:
            reflected |= flag_r

    return reflected
