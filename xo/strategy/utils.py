import numpy as np
from enum import Enum
from numba import njit


__all__ = [
    'StrategyType',
    'addition_hash',
]


class StrategyType(Enum):
    RANDOM = 1
    MINIMAX = 2


@njit
def addition_hash(arr, sz):
    # taken from: https://stackoverflow.com/questions/19854564/hash-integer-array
    hash_ = 17
    for i in range(sz):
        v = arr[i] 
        if np.isinf(v) or np.isnan(v):
            v = -1
        hash_ = (hash_ * 19) + v 
    return hash_