import sys
import numpy as np
from xo.strategy.minimax import StateCacheKey


class TestStateCacheKey:
    def test_hash(self):
        arr = np.full(3, np.nan)
        is_max = True
        key = StateCacheKey(arr, is_max)

        n_bins = 2 << sys.hash_info.width
        expected = 17
        expected = ((expected * 19) + -1) % n_bins
        expected = ((expected * 19) + -1) % n_bins
        expected = ((expected * 19) + -1) % n_bins
        expected = ((expected * 19) + is_max) % n_bins
        expected = int(expected)

        assert hash(key) == expected
