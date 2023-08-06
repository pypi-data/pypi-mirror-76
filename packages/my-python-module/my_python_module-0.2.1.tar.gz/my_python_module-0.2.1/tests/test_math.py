#!/usr/bin/env python
# -*-coding:utf-8-*-


from my_python_module.math import number_radix_conversion


def test_number_radix_conversion():
    assert number_radix_conversion(10, 'bin') == '1010'
    assert number_radix_conversion('0xff', 2, 16) == '11111111'
    assert number_radix_conversion(0o77, 'hex') == '3f'
    assert number_radix_conversion(100, 10) == '100'
