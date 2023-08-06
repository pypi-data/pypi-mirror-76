#!/usr/bin/env python
# -*- coding: utf-8 -*-

from my_python_module.exceptions import NotIntegerError
from my_python_module.common import str2pyobj
from my_python_module.basic.dict import merge_dict
from my_python_module.basic.list import del_list
from my_python_module.math import is_even, is_odd, is_prime, prime, fibonacci
import unittest
from pytest import raises


class Test(unittest.TestCase):
    def test_is_even(self):
        for i in [2, 4, -2, 0]:
            self.assertTrue(is_even(i))
        for i in [1, -1, 5]:
            self.assertFalse(is_even(i))
        for i in [1.1, 0.0, 2.2, -2.2]:
            self.assertRaises(NotIntegerError, is_even, i)

    def test_is_odd(self):
        for i in [2, 4, -2, 0]:
            self.assertFalse(is_odd(i))
        for i in [1, -1, 5]:
            self.assertTrue(is_odd(i))
        for i in [1.1, 0.0, 2.2, -2.2]:
            self.assertRaises(NotIntegerError, is_odd, i)

    def test_del_list(self):
        self.assertEqual(del_list([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [
            2, 5, 9]), [0, 1, 3, 4, 6, 7, 8])

    def test_str2pyobj(self):
        test_list = {}
        # test int
        test_list['int'] = '72'
        # test float
        test_list['float'] = '3.14'
        # test 'abc.html'
        test_list['str'] = 'abc.html'
        # test list
        test_list['list'] = '[1,2,3]'
        # test True
        test_list['bool'] = 'True'

        for t, inval in test_list.items():
            outval = str2pyobj(inval)
            self.assertEqual(str(type(outval)).split("\'")[1], t)

    def test_merge_dict(self):
        x = {'a': 1, 'b': 2}
        y = {'b': 10, 'c': 11}
        res = merge_dict(x, y)
        self.assertEqual(res, {'a': 1, 'c': 11, 'b': 10})


def test_is_prime():
    for i in [2, 3, 5, 7, 199, 499]:
        assert is_prime(i) is True
    for i in [1, -1, 0, 4, 6, 497]:
        assert is_prime(i) is False

    with raises(NotIntegerError):
        for i in [1.1, 0.0, 2.2, -2.2]:
            is_prime(i)


def test_prime():
    assert prime(4) == 7


def test_fibonacci():
    assert fibonacci(6) == 5
