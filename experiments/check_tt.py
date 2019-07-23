import xo
import pickle, os
import numpy as np


if __name__ == '__main__':
    fp = os.path.join('..', 'cache', 'minimax', '3-3-3.pickle')

    with open(fp, 'rb') as f:
        tt = pickle.load(f)

    print('Number of entries: {}'.format(len(tt)))
    for key, val in tt.items():
        print('{!r}'.format(key))
        print(val)
    non_zeros = map(lambda v: np.sum(np.isfinite(v[0])), tt.values())
    non_zeros = list(non_zeros)
    avg_non_zeros = np.mean(non_zeros)
    print('Avg no. of filled cells: {}'.format(avg_non_zeros))
