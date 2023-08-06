#!/usr/bin/env python
# -*-coding:utf-8-*-


def del_list(lst, indexs):
    """
    del list base a index list

>>> del_list([0,1,2,3,4,5],[2,3])
[0, 1, 4, 5]
>>> lst = list(range(6))
>>> lst
[0, 1, 2, 3, 4, 5]
>>> del_list(lst,[2,3])
[0, 1, 4, 5]
>>> lst
[0, 1, 4, 5]
>>> del_list(lst,[0,2])
[1, 5]
>>> lst
[1, 5]

    """
    count = 0
    for index in sorted(indexs):
        index = index - count
        del lst[index]
        count += 1
    return lst


def group_list(lst, n=1):
    """
    group a list, in some case, it is maybe useful.

>>> list(group_list(list(range(10)),0))
Traceback (most recent call last):
AssertionError
>>> list(group_list(list(range(10)),1))
[[0], [1], [2], [3], [4], [5], [6], [7], [8], [9]]
>>> list(group_list(list(range(10)),2))
[[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
>>> list(group_list(list(range(10)),3))
[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
>>> list(group_list(list(range(10)),4))
[[0, 1, 2, 3], [4, 5, 6, 7], [8, 9]]

    """
    assert n > 0
    for i in range(0, len(lst), n):
        yield lst[i:i + n]