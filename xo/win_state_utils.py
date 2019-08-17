import numpy as np
from xo.utils import make_logger


logger = make_logger('win_state_utils.py')


def compute_win_state_str_row(n_rows, n_cols, n_connects):
    """Each win state will be a string of 0s and 1s which can
    then converted into an integer in base 2. 

    I assume that at the maximum n_rows = n_cols = 5, which means
    that a 31 bit integer (since in Python it's always signed) 
    should be more than enough for a 25 bit string.
    """
    n_cells = n_rows * n_cols
    win_states = list()

    # each iteration in the for loop computes the possible
    # winning states for a particular row, e.g., 
    # - if n_connects == n_cols, there's just one winning state
    for row_ind in range(n_rows):
        prefix = '0' * (row_ind * n_cols)
        row_end = (row_ind * n_cols) + n_cols
        win_start_ind = row_ind * n_cols
        win_end_ind = win_start_ind + n_connects

        while win_end_ind <= row_end:
            # save the winning state
            suffix = '0' * (n_cells - win_end_ind)
            win_state = prefix + '1' * n_connects + suffix
            win_states.append(win_state)

            # update for the next possible win state of the row
            win_start_ind = win_start_ind + 1
            win_end_ind = win_start_ind + n_connects
            prefix += '0'

    return win_states


def transpose_win_state_str_row(win_state, n_rows, n_cols):
    """Assumes that the row win_state was computed with n_rows and
    n_cols swapped, i.e., (n_cols, n_rows) rather than (n_rows, n_cols).
    """
    mat = np.array(list(win_state), dtype=str)
    mat = mat.reshape((n_cols, n_rows))
    mat_transposed = mat.T
    win_state_col = ''.join(mat_transposed.ravel())
    return win_state_col


def compute_win_state_str_col(n_rows, n_cols, n_connects):
    """Exactly the same as row but transposed...
    """
    win_states_row = compute_win_state_str_row(n_cols, n_rows, n_connects)

    # info_msg = '{} row win states ({}, {}, {}): {}'
    # info_msg = info_msg.format(len(win_states_row),
    #                            n_cols, n_rows, n_connects,
    #                            win_states_row)
    # logger.info(info_msg)

    win_states_col = list()
    
    for win_state in win_states_row:
        transposed = transpose_win_state_str_row(win_state, n_rows, n_cols)
        win_states_col.append(transposed)

    return win_states_col


def compute_win_state_str_diag_l2r(n_rows, n_cols, n_connects):
    n_cells = n_rows * n_cols
    win_states = list()

    for row_ind in range(n_rows - n_connects + 1):
        prefix = '0' * (row_ind * n_cols)
        start_ind = row_ind * n_cols
        row_end = start_ind + n_cols

        cols_till_end = row_end - start_ind
        while cols_till_end >= n_connects:
            diag = '0' * n_cols + '1'
            diag = '1' + diag * (n_connects - 1)
            suffix = '0' * (n_cells - len(prefix) - len(diag))
            win_state = prefix + diag + suffix
            win_states.append(win_state)

            # update
            start_ind += 1
            cols_till_end = row_end - start_ind
            prefix += '0'

    return win_states


def reflect_y(win_state_str, n_rows, n_cols):
    n_cells = n_rows * n_cols
    reflected = np.full(n_cells, '0', dtype=str)

    for ind in range(n_cells):
        row_ind = ind // n_cols
        col_ind = ind % n_cols
        col_ind_r = n_cols - (col_ind + 1)
        ind_r = row_ind * n_cols + col_ind_r
        reflected[ind_r] = win_state_str[ind]

    reflected = ''.join(reflected.ravel())
    return reflected


def compute_win_state_str_diag_r2l(n_rows, n_cols, n_connects):
    """Just the l2r win state strings but reflected on the y axis.
    """
    win_state_str = compute_win_state_str_diag_l2r(n_rows, n_cols, n_connects)
    return [reflect_y(s, n_rows, n_cols) for s in win_state_str]


def compute_win_state_row(n_rows, n_cols, n_connects):
    win_state_str = compute_win_state_str_row(n_rows, n_cols, n_connects)

    # debugging
    # info_msg = 'Row win states: {}'.format(win_state_str)
    # logger.info(info_msg)

    return [int(s, 2) for s in win_state_str]


def compute_win_state_col(n_rows, n_cols, n_connects):
    win_state_str = compute_win_state_str_col(n_rows, n_cols, n_connects)
    return [int(s, 2) for s in win_state_str]


def compute_win_state_diag_l2r(n_rows, n_cols, n_connects):
    win_state_str = compute_win_state_str_diag_l2r(n_rows, n_cols, n_connects)
    return [int(s, 2) for s in win_state_str]


def compute_win_state_diag_r2l(n_rows, n_cols, n_connects):
    win_state_str = compute_win_state_str_diag_r2l(n_rows, n_cols, n_connects)
    return [int(s, 2) for s in win_state_str]


def get_board_wins(n_rows, n_cols, n_connects):
    row_wins = compute_win_state_row(n_rows, n_cols, n_connects)
    col_wins = compute_win_state_col(n_rows, n_cols, n_connects)
    l2r_diag_wins = compute_win_state_diag_l2r(n_rows, n_cols, n_connects)
    r2l_diag_wins = compute_win_state_diag_r2l(n_rows, n_cols, n_connects)
    return row_wins + col_wins + l2r_diag_wins + r2l_diag_wins
