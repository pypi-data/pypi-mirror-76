#!/usr/bin/env python
# -*-coding:utf-8-*-


"""

选择排序： 最直观的一种排序方法

"""


def selection_sort(seq):
    res = list(seq.copy())
    for i in range(0, len(res)):
        minimum = i
        for j in range(i + 1, len(res)):
            if res[j] < res[minimum]:
                minimum = j
        res[i], res[minimum] = res[minimum], res[i]

    return res


def selection_sort2(seq):
    """
    :param seq:
    :return:
    """

    def find_smallest_index(seq):
        smallest = seq[0]
        smallest_index = 0
        for i in range(1, len(seq)):
            target = seq[i]
            if target < smallest:
                smallest = target
                smallest_index = i
        return smallest_index

    res = []
    seq_copy = seq.copy()

    for i in range(0, len(seq)):
        smallest_index = find_smallest_index(seq_copy)
        res.append(seq_copy.pop(smallest_index))

    return res
