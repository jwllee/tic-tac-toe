def get_board_wins(n_rows, n_cols, n_connects):
    wins = None
    if (n_rows, n_cols, n_connects) == (3, 3, 3):
        wins = wins_3x3x3
    elif (n_rows, n_cols, n_connects) == (4, 4, 4):
        wins = wins_4x4x4 
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
