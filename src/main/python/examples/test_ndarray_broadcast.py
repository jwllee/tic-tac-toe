import numpy as np


if __name__ == '__main__':
    l = np.asarray(range(10))
    print((l == l[0]).all())
