import numpy as np


def check_col_win_state(expected, actual):
    info_msg = 'Converted to win_state_col {}'
    info_msg = info_msg.format(actual)
    print(info_msg)
    assert_msg = '{} != {}'.format(expected, actual)
    assert expected == actual, assert_msg


if __name__ == '__main__':
    # try to transform row win state to col win state
    # row win state for 3x3 board
    win_state_row = '111000000'
    mat = np.array(list(win_state_row), dtype=str)
    mat = mat.reshape((3, 3))
    info_msg = 'win_state_row {} to mat: \n{}'
    info_msg = info_msg.format(win_state_row, mat)
    print(info_msg)

    mat_transposed = mat.T
    win_state_col = ''.join(mat_transposed.ravel())
    expected_col = '100100100'

    check_col_win_state(expected_col, win_state_col)

    print('\n')

    # harder example with n_rows != n_cols
    # n_rows = 4 and n_cols = 3 and n_connects = 3
    # compute the row win state using n_rows = 3, n_cols = 4, n_connects = 3
    win_state_row = '111000000000'
    mat = np.array(list(win_state_row), dtype=str)
    mat = mat.reshape((3, 4))
    info_msg = 'win_state_row {} to mat: \n{}'
    info_msg = info_msg.format(win_state_row, mat)
    print(info_msg)

    mat_transposed = mat.T
    win_state_col = ''.join(mat_transposed.ravel())
    expected_col = '100100100000'
    
    check_col_win_state(expected_col, win_state_col)
