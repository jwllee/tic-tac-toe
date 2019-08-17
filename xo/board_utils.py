import numpy as np


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


def is_filled(board_x, board_o, full_state):
    current_state = board_o | board_x
    filled = (current_state & full_state) == full_state
    return filled


def is_game_over(board_x, board_o, n_rows, n_cols, n_connects):
    # check for drawn first
    board_win = get_board_wins(n_rows, n_cols, n_connects)
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


def get_board_wins(n_rows, n_cols, n_connects):
    wins = None
    if (n_rows, n_cols, n_connects) == (3, 3, 3):
        wins = wins_3x3x3
    elif (n_rows, n_cols, n_connects) == (4, 4, 4):
        wins = wins_4x4x4 
    elif (n_rows, n_cols, n_connects) == (4, 4, 3):
        wins = wins_4x4x3
    elif (n_rows, n_cols, n_connects) == (5, 5, 5):
        wins = wins_5x5x5
    else:
        err_msg = 'Do not have wins cache for ({}, {}, {}) game'
        err_msg = err_msg.format(n_rows, n_cols, n_connects)
        raise ValueError(err_msg)
    return wins


wins_3x3x3 = [
    0b000000111,    # rows
    0b000111000,
    0b111000000,
    0b001001001,    # columns
    0b010010010,
    0b100100100,
    0b100010001,    # diagonals
    0b001010100,
]


wins_4x4x4 = [
    0b0000000000001111, # rows
    0b0000000011110000,
    0b0000111100000000,
    0b1111000000000000,
    0b0001000100010001, # columns
    0b0010001000100010,
    0b0100010001000100,
    0b1000100010001000, 
    0b1000010000100001, # diagonals
    0b0001001001001000,
]


wins_4x4x3 = [
    0b0000000000000111, # rows
    0b0000000000001110, 
    0b0000000001110000,
    0b0000000011100000,
    0b0000011100000000,
    0b0000111000000000,
    0b0111000000000000,
    0b1110000000000000,
    0b0000000100010001, # columns
    0b0001000100010000, 
    0b0000001000100010,
    0b0010001000100000,
    0b0000010001000100,
    0b0100010001000000,
    0b0000100010001000, 
    0b1000100010000000, 
    0b0000010000100001, # diagonals
    0b1000010000100000, 
    0b0000001001001000,
    0b0001001001000000,
]


wins_5x5x5 = [
    0b0000000000000000000011111, # rows
    0b0000000000000001111100000,
    0b0000000000111110000000000,
    0b0000011111000000000000000,
    0b1111100000000000000000000,
    0b0000100001000010000100001, # columns
    0b0001000010000100001000010,
    0b0010000100001000010000100,
    0b0100001000010000100001000,
    0b1000010000100001000010000,
    0b1000001000001000001000001, # diagonals
    0b0000100010001000100010000,
]
