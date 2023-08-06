#!/usr/bin/env python
# -*-coding:utf-8-*-


from my_python_module.algorithms.graph.find_path import breadth_first_search, find_shortest_path, depth_first_search, \
    find_shortest_path_bfs, find_shortest_path_dijkstra
from my_python_module.algorithms.graph.graph import DirectedGraph, WeightedDirectedGraph


def test_bfs():
    graph_data = {
        'a': ['b', 'c'],
        'b': ['e', 'd'],
        'd': ['f'],
        'c': [],
        'e': [],
        'f': []
    }
    graph1 = DirectedGraph(graph_data)
    data = breadth_first_search(graph1, start='a', end='f')
    print(data)

    graph_data2 = {
        'you': ['alice', 'bob', 'claire'],
        'bob': ['anuj', 'peggy'],
        'alice': ['peggy'],
        'claire': ['thom', 'jonny'],
        'anuj': [],
        'peggy': [],
        'thom': [],
        'jonny': []
    }
    graph2 = DirectedGraph(graph_data2)

    data = find_shortest_path(graph2, start='you', end='anuj')
    assert data == ['you', 'bob', 'anuj']
    data = find_shortest_path_bfs(graph2, start='you', end='anuj')
    assert data == ['you', 'bob', 'anuj']

    data = find_shortest_path(graph2, start='you', end='peggy')
    assert data == ['you', 'alice', 'peggy'] or data == ['you', 'bob', 'peggy']


def test_dfs():
    graph = {
        'you': ['alice', 'bob', 'claire'],
        'bob': ['anuj', 'peggy'],
        'alice': ['peggy'],
        'claire': ['thom', 'jonny'],
        'anuj': [],
        'peggy': [],
        'thom': [],
        'jonny': []
    }

    graph = DirectedGraph(graph)
    data = depth_first_search(graph, start='you', end='anuj')

    print(data)


def test_dijkstra():
    graph = WeightedDirectedGraph()
    graph.add_node('start')
    graph.add_edge(('start', 'a'))
    graph.add_edge(('start','b'))
    graph.add_edge(('a','end'))
    graph.add_edge(('b','end'))
    graph.set_edge_weight(('start', 'a'), 6)
    graph.set_edge_weight(('start','b'), 2)
    graph.set_edge_weight(('a','end'), 1)
    graph.set_edge_weight(('b','end'), 5)
    graph.add_edge(('b','a'))
    graph.set_edge_weight(('b','a'),3)

    data = find_shortest_path_dijkstra(graph, 'start', 'end')

    assert data == ['start', 'b', 'a', 'end']