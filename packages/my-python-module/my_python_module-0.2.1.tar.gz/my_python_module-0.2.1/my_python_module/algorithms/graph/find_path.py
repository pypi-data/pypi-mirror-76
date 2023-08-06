#!/usr/bin/env python
# -*-coding:utf-8-*-


"""
针对有向图


"""

from collections import deque, defaultdict
from .graph import Graph, WeightedDirectedGraph

import logging

logger = logging.getLogger(__name__)


def breadth_first_search(graph: Graph, start, end):
    """
    Breadth-first search.

    @type  graph: graph, digraph
    @param graph: Graph.

    @type  start: node
    @param start: Optional root node (will explore only root's connected component)

    @rtype:  tuple
    @return: A tuple containing a dictionary and a list.
        1. Generated spanning tree
        2. Graph's level-based ordering
    """

    def bfs():
        """
        Breadth-first search subfunction.
        """
        while (queue != []):
            node = queue.popleft()

            if (node not in spanning_tree):
                for other in graph.neighbors(node):
                    if other == end:
                        spanning_tree[node].append(other)
                        return True
                    else:
                        spanning_tree[node].append(other)
                        queue.extend(graph.neighbors(node))

    queue = deque()  # Visiting queue
    spanning_tree = defaultdict(list)  # Visited

    queue.append(start)
    bfs()
    logger.info('bfs spanning_tree: {0}'.format(spanning_tree))
    return spanning_tree


def depth_first_search(graph: Graph, start, end):
    """
    Depth-first search.
    """
    finded = False

    def dfs(node):
        """
        Depth-first search subfunction.
        """
        nonlocal finded
        if finded:
            return True

        for other in graph.neighbors(node):
            if other == end:
                spanning_tree[node].append(other)
                finded = True
                return True
            else:
                spanning_tree[node].append(other)
                dfs(other)

    spanning_tree = defaultdict(list)

    dfs(start)

    logger.info('dfs spanning_tree: {0}'.format(spanning_tree))
    return spanning_tree


def explain_spanning_tree(spanning_tree, start, end, path=[]):
    if end == start:
        path.insert(0, start)
        return path
    else:
        for k, v in spanning_tree.items():
            if end in v:
                path.insert(0, end)
                return explain_spanning_tree(spanning_tree, start, k, path=path)


def find_shortest_path_bfs(graph: Graph, start, end):
    spanning_tree = breadth_first_search(graph=graph, start=start, end=end)

    return explain_spanning_tree(spanning_tree, start, end)


def find_shortest_path(graph: Graph, start, end, path=[]):
    """
    another version of find shortest path,
    I think it is a dfs version, what's your opition.
    :return:
    """
    path = path + [start]
    if start == end:
        return path
    if start not in graph:
        return None
    shortest = None
    for node in graph.neighbors(start):
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest


def find_shortest_path_dijkstra(graph: WeightedDirectedGraph, start, end, ):
    processed = []
    costs = {}
    parents = {}  # 子节点---> 父节点

    # costs 初始化 直达的赋值，不能直达的赋无穷大
    #

    def init_costs(graph: WeightedDirectedGraph, start):
        nonlocal costs

        for node in graph.nodes():
            if node == start:
                pass
            elif node in graph.neighbors(start):
                costs[node] = graph.edge_weight((start, node))
            else:
                costs[node] = float("inf")

    def init_parents(graph: WeightedDirectedGraph, start):
        nonlocal parents

        for node in graph.nodes():
            if node == start:
                pass
            elif node in graph.neighbors(start):
                parents[node] = start
            else:
                parents[node] = None  # 与costs同步

    def find_lowest_cost_node(costs):
        """
        start - node the total cost
        always return the lowest cost node.
        :param costs:
        :return:
        """
        lowest_cost = float("inf")
        lowest_cost_node = None
        nonlocal processed

        for node, cost in costs.items():
            if cost < lowest_cost and node not in processed:
                lowest_cost = cost
                lowest_cost_node = node
        return lowest_cost_node

    def explain_parents(start, end, path=[]):
        nonlocal parents

        if start == end:
            path.append(start)
            return path
        else:
            for k, v in parents.items():
                if v == start:
                    path.append(start)
                    return explain_parents(k, end, path=path)

    init_costs(graph, start)
    init_parents(graph, start)

    node = find_lowest_cost_node(costs)
    while node is not None:
        cost = costs[node]
        for sub_node in graph.neighbors(node):
            new_cost = cost + graph.edge_weight((node, sub_node))
            if costs[sub_node] > new_cost:  # 需要更新
                costs[sub_node] = new_cost
                parents[sub_node] = node  # node -> sub_node

        processed.append(node)
        node = find_lowest_cost_node(costs)

    return explain_parents(start, end)
