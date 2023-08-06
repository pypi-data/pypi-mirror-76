#!/usr/bin/env python
# -*-coding:utf-8-*-

import pytest
from my_python_module.algorithms.sort.selection_sort import selection_sort, selection_sort2


def test_selection_sort2():
    assert selection_sort2([1, 2, 4, 5, 22, 6, 23]) == [1, 2, 4, 5, 6, 22, 23]


def test_selection_sort():
    assert selection_sort([1, 2, 4, 5, 22, 6, 23]) == [1, 2, 4, 5, 6, 22, 23]


@pytest.mark.skip(reason="i have test it")
def test_section_timeit():
    import numpy as np
    data = np.random.randn(10000)
    seq = list(data)
    import time

    t1 = time.time()

    selection_sort2(seq)
    t2 = time.time()

    selection_sort(seq)
    t3 = time.time()
    print('select_sort use time {0}'.format(t3 - t2))

    print('select_sort2 use time {0}'.format(t2 - t1))
