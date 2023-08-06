#!/usr/bin/env python
# -*-coding:utf-8-*-


"""
use python bisect module speed it up
"""

import logging
from bisect import insort_left, bisect_left

logger = logging.getLogger(__name__)


def binary_search_slow(seq, target, func=lambda x: x, round_n = 4, approx=False):
    """
    单调函数的二分逼近

    func 定义的函数 ，参数由 seq 决定
    target 匹配的结果
    round_n 精确到小数点多少位
    approx 模糊匹配模式

    返回值：
        approx=False  找到的索引值，或者-1 没有找到
        approx=True 精确匹配的索引值 或者 近似匹配的索引值
    :param f:
    :param seq:
    :param target:
    :return:
    """
    low = 0
    high = len(seq) - 1
    count = 0
    while low < high:
        count += 1
        mid = (high + low) // 2

        if approx:
            guess = round(func(seq[mid]), round_n)
            target = round(target, round_n)
        else:
            guess = func(seq[mid])

        if guess < target: # 包括等于target的情况都会扔到大数区
            low = mid + 1
        else:
            high = mid

    # approx
    logger.info('binary_search_slow run {0} times'.format(count))
    if approx:
        return low
    else:
        return (low if (low != len(seq) and seq[low] == target) else -1)


def binary_search(seq, target):
    """
    seq已排序，二分查找
    返回的是已经找到的索引值或者没有找到返回-1
    :param seq:
    :param target:
    :return:
    """
    pos = bisect_left(seq, target)
    return (pos if (pos != len(seq) and seq[pos] == target) else -1)


def binary_insert(seq, target):
    """
    seq 已经排序， 如果target 已存在，则插入最左边
    :param seq:
    :param target:
    :return:
    """
    seq_copy = seq.copy()
    insort_left(seq_copy, target)
    return seq_copy

