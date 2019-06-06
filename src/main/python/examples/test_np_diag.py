import numpy as np


if __name__ == '__main__':
    n_rows = n_cols = 3
    n_elems = n_rows * n_cols
    mat = np.arange(n_elems).reshape(n_rows, n_cols)

    print(mat)

    print('Getting diagonal...')
    print(mat.diagonal(0))
    print(mat.diagonal(1))
    print(np.diag(np.fliplr(mat), 1))
