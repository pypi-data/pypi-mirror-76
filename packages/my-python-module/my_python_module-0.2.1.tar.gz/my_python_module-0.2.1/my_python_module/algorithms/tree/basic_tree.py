#!/usr/bin/env python
# -*-coding:utf-8-*-


class Tree(object):
    def __init__(self, data=None, parent=None):
        self.data = data
        self.left = None
        self.right = None

        self.parent = parent
    def __repr__(self):
        return '<Tree {}>'.format(self.data)