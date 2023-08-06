#!/usr/bin/env python
# -*-coding:utf-8-*-

import pytest
import logging
logging.basicConfig(level=logging.DEBUG)

from my_python_module.algorithms.search.binary_search import binary_search, binary_insert, binary_search_slow


def test_binary_search():
    seq = [1, 2, 10, 20]
    assert binary_search(seq, 6) == -1
    assert binary_search(seq, 2) == 1


def test_binary_insert():
    seq = [1, 2, 10, 20]
    assert binary_insert(seq, 6) == [1, 2, 6, 10, 20]


def test_func_binary_search():
    import numpy as np
    round_n = 6
    seq = np.arange(0, 10, 10**(-round_n))

    mid= binary_search_slow(seq, 2, func=lambda x: x*x, round_n = 6, approx=True)

    assert pytest.approx(seq[mid]) ==  1.414214

    seq = [1, 2, 10, 20]
    assert binary_search_slow(seq, 6) == -1
    assert binary_search_slow(seq, 2) == 1