#!/usr/bin/env python
# -*-coding:utf-8-*-


class BinarySearchTree(object):
    """
    二叉搜索树 left right 由 data的 hash值决定
    """

    def __init__(self, data=None, parent=None):
        self.left = None
        self.right = None
        self.data = data
        self.parent = parent

    def __repr__(self):
        return '<BinarySearchTree {}>'.format(self.data)

    def insert(self, data):
        if hash(data) < hash(self.data):
            if self.left is None:
                self.left = BinarySearchTree(data, parent=self)
            else:
                self.left.insert(data)
        elif hash(data) > hash(self.data):
            if self.right is None:
                self.right = BinarySearchTree(data, parent=self)
            else:
                self.right.insert(data)
        else:
            self.data = data

    def search(self, data):
        if hash(data) < hash(self.data):
            if self.left is None:
                return False
            else:
                return self.left.search(data)
        elif hash(data) > hash(self.data):
            if self.right is None:
                return False
            else:
                return self.right.search(data)
        else:
            return self

    def introspection(self):
        """walk a round,and get myself information"""
        stack = []
        node = self
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                yield node
                node = node.right
        return stack

    def children_count(self):
        """Return the number of children

        @returns number of children: 0, 1, 2
        """
        cnt = 0
        if self.left:
            cnt += 1
        if self.right:
            cnt += 1
        return cnt

    def delete(self, data):
        """Delete node containing data

        @param data node's content to delete
        """
        # get node containing data
        node, parent = self.lookup(data)
        if node is not None:
            children_count = node.children_count()
            if children_count == 0:
                # if node has no children, just remove it
                if parent:
                    if parent.left is node:
                        parent.left = None
                    else:
                        parent.right = None
                else:
                    self.data = None
            elif children_count == 1:
                # if node has 1 child
                # replace node by its child
                if node.left:
                    n = node.left
                else:
                    n = node.right
                if parent:
                    if parent.left is node:
                        parent.left = n
                    else:
                        parent.right = n
                else:
                    self.left = n.left
                    self.right = n.right
                    self.data = n.data
            else:
                # if node has 2 children
                # find its successor
                parent = node
                successor = node.right
                while successor.left:
                    parent = successor
                    successor = successor.left
                # replace node data by its successor data
                node.data = successor.data
                # fix successor's parent node child
                if parent.left == successor:
                    parent.left = successor.right
                else:
                    parent.right = successor.right

    def compare_trees(self, node):
        """Compare 2 trees

        @param node tree to compare
        @returns True if the tree passed is identical to this tree
        """
        if node is None:
            return False
        if self.data != node.data:
            return False
        res = True
        if self.left is None:
            if node.left:
                return False
        else:
            res = self.left.compare_trees(node.left)
        if res is False:
            return False
        if self.right is None:
            if node.right:
                return False
        else:
            res = self.right.compare_trees(node.right)
        return res


if __name__ == '__main__':
    tree = BinarySearchTree()
    tree.insert(10)
    tree.insert(15)
    tree.insert(6)
    tree.insert(4)
    tree.insert(9)
    tree.insert(12)
    tree.insert(24)
    tree.insert(7)
    tree.insert(20)
    tree.insert(30)
    tree.insert(18)

    assert tree.search(24)
    assert not tree.search(50)
