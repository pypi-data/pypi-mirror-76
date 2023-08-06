#!/usr/bin/env python
# -*-coding:utf-8-*-


import logging

logger = logging.getLogger(__name__)


class MindMapTree(object):
    def __init__(self, data=None, parent=None):
        self.data = data
        self.parent = parent
        self.children = []

    def introspection(self):
        """
        核心内省函数，返回我和我的所有children。
        """
        stack = []
        tree = self
        if tree.data is not None:
            logger.debug('intorspection add node:{0}'.format(tree))
            stack.append(tree)

            for child in tree:
                stack += child.introspection()
        return stack

    def __str__(self):
        if self.children:
            return '<MindMapTree:{0}> has children: {1}'.format(self.data, self.children)
        else:
            return '<MindMapTree:{0}>'.format(self.data)

    def __repr__(self):
        if self.children:
            return '<MindMapTree:{0}> has children: {1}'.format(self.data, self.children)
        else:
            return '<MindMapTree:{0}>'.format(self.data)

    def append(self, child_data):
        child = MindMapTree(child_data, parent=self)
        self.children.append(child)

    def remove(self, child_data):
        child = MindMapTree(child_data, parent=self)
        self.children.remove(child)

    def insert(self, parent_data, child_data):
        for target in self.introspection():
            if target.data == parent_data:
                target.append(child_data)

    def find(self, key):
        for target in self.introspection():
            if target.data == key:
                return target
        raise KeyError

    def set_nodedata(self, data):
        self.data = data

    def __iter__(self):
        if self.children is not None:
            for child in self.children:
                yield child

    def to_json(self):
        return {self.data: [i.to_json() for i in self.children]}

    def get_path(self):
        res = []
        while True:
            res.append(self.data)
            if self.parent is None:
                break
            else:
                self = self.parent
        return res[::-1]


if __name__ == "__main__":
    tree = MindMapTree("奴隶社会")
    tree.append("非洲")
    tree.append("亚洲")
    tree.insert("非洲", "古埃及文明")
    tree.insert("古埃及文明", "金字塔")
    tree.insert("亚洲", "两河流域文明")
    tree.insert("两河流域文明", "汉谟拉比法典")
    tree.insert("亚洲", "古印度")

    print(tree)
    print('######################')
    stack = tree.introspection()

    print(stack)

    yazhou = tree.find("亚洲")

    print(yazhou.introspection())
    print(yazhou.parent)
    print(yazhou.children)

    print(tree.to_json())

    print(tree.get_path())
