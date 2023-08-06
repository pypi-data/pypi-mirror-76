#!/usr/bin/env python
# -*-coding:utf-8-*-

"""

快速排序

"""


def quick_sort(seq):
    """
    10000 的随机数列表排序：
    select_sort use time 3.0919713973999023
    quick sort use time 0.024930477142333984

    :param seq:
    :return:
    """
    if len(seq) < 2:
        return seq
    else:
        pivot = seq[0]

        less_part = [i for i in seq[1:] if i <= pivot]

        greater_part = [i for i in seq[1:] if i > pivot]

        return quick_sort(less_part) + [pivot] + quick_sort(greater_part)



