#!/usr/bin/env python
# -*-coding:utf-8-*-


import os
import json

"""
treat json file as one dict value, and do some operation.
"""

def write_json(file, data):
    with open(file, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def get_json_file(json_filename):
    """
    :return:
    """
    if not os.path.exists(json_filename):
        data = {}
        write_json(json_filename, data)

    return json_filename


def get_json_data(json_filename):
    """
    get json file data
    :return:
    """
    with open(get_json_file(json_filename), encoding='utf8') as f:
        res = json.load(f)
        return res


def get_json_value(json_filename, k):
    res = get_json_data(json_filename)
    return res.get(k)


def set_json_value(json_filename, k, v):
    """
    set json value on target file
    """
    res = get_json_data(json_filename)
    res[k] = v
    write_json(get_json_file(json_filename), res)
