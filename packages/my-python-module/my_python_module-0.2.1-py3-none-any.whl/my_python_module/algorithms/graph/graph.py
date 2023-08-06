#!/usr/bin/env python
# -*-coding:utf-8-*-

"""

图论模型

graph 实际存储数据

node 节点

edge 边



"""
from abc import abstractmethod
from abc import ABC

from my_python_module.exceptions import AdditionError


class Graph(ABC):
    """
    一般图
    """
    DIRECTED = None

    @abstractmethod
    def nodes(self):
        """
        :return:
        """
        raise NotImplementedError("Not Implement nodes methods")

    @abstractmethod
    def neighbors(self, node):
        """
        :return:
        """
        raise NotImplementedError("Not Implement neighbors methods")

    @abstractmethod
    def edges(self):
        """
        :return:
        """
        raise NotImplementedError("Not Implement edges methods")

    @abstractmethod
    def has_node(self, node):
        """
        :return:
        """
        raise NotImplementedError("Not Implement has_node methods")

    @abstractmethod
    def has_edge(self, edge):
        """
        :return:
        """
        raise NotImplementedError("Not Implement has_edge methods")

    @abstractmethod
    def add_node(self, node):
        """
        :return:
        """
        raise NotImplementedError("Not Implement add_node methods")

    @abstractmethod
    def add_edge(self, node):
        """
        :return:
        """
        raise NotImplementedError("Not Implement add_edge methods")

    def __str__(self):
        """
        Return a string representing the graph when requested by str() (or print).

        @rtype:  string
        @return: String representing the graph.
        """
        str_nodes = repr(self.nodes())
        str_edges = repr(self.edges())
        return "{0} {1}".format(str_nodes, str_edges)

    def __repr__(self):
        """
        Return a string representing the graph when requested by repr()

        @rtype:  string
        @return: String representing the graph.
        """
        return "<{0}.{1} {2}>".format(self.__class__.__module__,
                                      self.__class__.__name__, str(self))

    def __iter__(self):
        """
        Return a iterator passing through all nodes in the graph.

        @rtype:  iterator
        @return: Iterator passing through all nodes in the graph.
        """
        for n in self.nodes():
            yield n

    def __len__(self):
        """
        Return the order of self when requested by len().

        @rtype:  number
        @return: Size of the graph.
        """
        return self.order()

    def __getitem__(self, node):
        """
        Return a iterator passing through all neighbors of the given node.

        @rtype:  iterator
        @return: Iterator passing through all neighbors of the given node.
        """
        for n in self.neighbors(node):
            yield n

    def order(self):
        """
        Return the order of self, this is defined as the number of nodes in the graph.

        @rtype:  number
        @return: Size of the graph.
        """
        return len(self.nodes())

    def add_nodes(self, nodelist):
        """
        Add given nodes to the graph.

        @attention: While nodes can be of any type, it's strongly recommended to use only
        numbers and single-line strings as node identifiers if you intend to use write().
        Objects used to identify nodes absolutely must be hashable. If you need attach a mutable
        or non-hashable node, consider using the labeling feature.

        @type  nodelist: list
        @param nodelist: List of nodes to be added to the graph.
        """
        for each in nodelist:
            self.add_node(each)

    def add_spanning_tree(self, st):
        """
        Add a spanning tree to the graph.

        @type  st: dictionary
        @param st: Spanning tree.
        """
        self.add_nodes(list(st.keys()))
        for each in st:
            if (st[each] is not None):
                self.add_edge((st[each], each))

    def complete(self):
        """
        Make the graph a complete graph.

        @attention: This will modify the current graph.
        """
        for each in self.nodes():
            for other in self.nodes():
                if (each != other and not self.has_edge((each, other))):
                    self.add_edge((each, other))

    def __eq__(self, other):
        """
        Return whether this graph is equal to another one.

        @type other: graph, digraph
        @param other: Other graph or digraph

        @rtype: boolean
        @return: Whether this graph and the other are equal.
        """

        def nodes_eq():
            for each in self:
                if (not other.has_node(each)): return False
            for each in other:
                if (not self.has_node(each)): return False
            return True

        def edges_eq():
            for edge in self.edges():
                if (not other.has_edge(edge)): return False
            for edge in other.edges():
                if (not self.has_edge(edge)): return False
            return True

        try:
            return nodes_eq() and edges_eq()
        except AttributeError:
            return False


class UndirectedGraph(Graph):
    """
    无向图

    {
        'a': {'b','z'}
    }
    """
    DIRECTED = False

    def __init__(self, graph_dict=None):
        """
        Initialize a graph.
        """

        if graph_dict is None:
            self.graph_dict = {}  # Pairing: Node -> Neighbors
        else:
            self.graph_dict = graph_dict

    def nodes(self):
        """
        Return node list.

        @rtype:  list
        @return: Node list.
        """
        return list(self.graph_dict.keys())

    def neighbors(self, node):
        """
        Return all nodes that are directly accessible from given node.

        @type  node: node
        @param node: Node identifier

        @rtype:  list
        @return: List of nodes directly accessible from given node.
        """
        return list(self.graph_dict[node])

    def _generate_edges(self):
        """ A static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for node in self.nodes():
            for neighbour in self.neighbors(node):
                if {neighbour, node} not in edges:
                    edges.append({node, neighbour})
        return edges

    def edges(self):
        """
        Return all edges in the graph.

        @rtype:  list
        @return: List of all edges in the graph.
        """
        return self._generate_edges()

    def has_node(self, node):
        """
        Return whether the requested node exists.

        @type  node: node
        @param node: Node identifier

        @rtype:  boolean
        @return: Truth-value for node existence.
        """
        return node in self.graph_dict

    def add_node(self, node):
        """
        Add given node to the graph.

        @attention: While nodes can be of any type, it's strongly recommended to use only
        numbers and single-line strings as node identifiers if you intend to use write().

        @type  node: node
        @param node: Node identifier.
        """
        if (not node in self.graph_dict):
            self.graph_dict[node] = set()
        else:
            raise AdditionError("Node %s already in graph" % node)

    def add_edge(self, edge):
        """
        Add an edge to the graph connecting two nodes.

        An edge, here, is a pair of nodes like C{(n, m)}.

        @type  edge: tuple
        @param edge: Edge.

        """
        if len(edge) == 1:
            u = v = edge.pop()
        elif len(edge) == 2:
            u, v = edge

        if u not in self.graph_dict:
            self.add_node(u)

        if v not in self.graph_dict:
            self.add_node(v)

        if (v not in self.graph_dict[u] and u not in self.graph_dict[v]):
            self.graph_dict[u].add(v)
            if (u != v):
                self.graph_dict[v].add(u)
        else:
            raise AdditionError("Edge ({0}, {1}) already in graph".format(u, v))

    def del_node(self, node):
        """
        Remove a node from the graph.

        @type  node: node
        @param node: Node identifier.
        """
        for each in list(self.neighbors(node)):
            if (each != node):
                self.del_edge((each, node))
        del (self.graph_dict[node])

    def del_edge(self, edge):
        """
        Remove an edge from the graph.

        @type  edge: tuple
        @param edge: Edge.
        """
        u, v = edge
        self.graph_dict[u].remove(v)
        if (u != v):
            self.graph_dict[v].remove(u)

    def has_edge(self, edge):
        """
        Return whether an edge exists.

        @type  edge: tuple
        @param edge: Edge.

        @rtype:  boolean
        @return: Truth-value for edge existence.
        """
        u, v = edge
        return {u, v} in self.edges()

    def node_order(self, node):
        """
        Return the order of the graph

        @rtype:  number
        @return: Order of the given node.
        """
        return len(self.neighbors(node))

    def __ne__(self, other):
        """
        Return whether this graph is not equal to another one.

        @type other: graph, digraph
        @param other: Other graph or digraph

        @rtype: boolean
        @return: Whether this graph and the other are different.
        """
        return not (self == other)


class DirectedGraph(Graph):
    """
     有向图

     {
         'a': ['b','z'] 只记录指向
     }
     """
    DIRECTED = True

    def __init__(self, graph_dict=None):
        """
        Initialize a graph.
        """

        if graph_dict is None:
            self.graph_dict = {}  # Pairing: Node -> Neighbors
        else:
            self.graph_dict = graph_dict

    def nodes(self):
        """
        Return node list.

        @rtype:  list
        @return: Node list.
        """
        return list(self.graph_dict.keys())

    def neighbors(self, node):
        """
        Return all nodes that are incident to the given node.

        @type  node: node
        @param node: Node identifier

        @rtype:  list
        @return: List of nodes directly accessible from given node.
        """
        return self.graph_dict[node]

    def edges(self):
        """
        Return all edges in the graph.

        @rtype:  list
        @return: List of all edges in the graph.
        """
        return self._generate_edges()

    def _generate_edges(self):
        """ A static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for node in self.nodes():
            for neighbor in self.neighbors(node):
                if (node, neighbor) not in edges:
                    edges.append((node, neighbor))
        return edges

    def has_node(self, node):
        """
        Return whether the requested node exists.

        @type  node: node
        @param node: Node identifier

        @rtype:  boolean
        @return: Truth-value for node existence.
        """
        return node in self.graph_dict

    def add_node(self, node):
        """
        Add given node to the graph.

        @attention: While nodes can be of any type, it's strongly recommended to use only
        numbers and single-line strings as node identifiers if you intend to use write().

        @type  node: node
        @param node: Node identifier.

        """

        if (node not in self.graph_dict):
            self.graph_dict[node] = []
        else:
            raise AdditionError("Node {0} already in digraph".format(node))

    def add_edge(self, edge):
        """
        Add an directed edge to the graph connecting two nodes.

        An edge, here, is a pair of nodes like C{(n, m)}.

        @type  edge: tuple
        @param edge: Edge.
        """
        u, v = edge
        for n in [u, v]:
            if not n in self.graph_dict:
                self.add_node(n)

        if v in self.graph_dict[u] and u in self.graph_dict[v]:
            raise AdditionError("Edge (%s, %s) already in digraph" % (u, v))
        else:
            self.graph_dict[u].append(v)

    def del_node(self, node):
        """
        Remove a node from the graph.

        @type  node: node
        @param node: Node identifier.
        """
        for edge in self.edges():
            a, b = edge
            if b == node:
                self.del_edge((a, node))

        # Remove this node from the neighbors and incidents tables
        del (self.graph_dict[node])

    def del_edge(self, edge):
        """
        Remove an directed edge from the graph.

        @type  edge: tuple
        @param edge: Edge.
        """
        u, v = edge
        if v in self.graph_dict[u]:
            self.graph_dict[u].remove(v)

    def has_edge(self, edge):
        """
        Return whether an edge exists.

        @type  edge: tuple
        @param edge: Edge.

        @rtype:  boolean
        @return: Truth-value for edge existence.
        """
        u, v = edge
        return (u, v) in self.edges()

    def __ne__(self, other):
        """
        Return whether this graph is not equal to another one.

        @type other: graph, digraph
        @param other: Other graph or digraph

        @rtype: boolean
        @return: Whether this graph and the other are different.
        """
        return not (self == other)


class WeightedDirectedGraph(DirectedGraph):
    """
     带权重的有向图， 权重作为 weight 属性值而存在。

     {
         'a': {'b':{},'z':{}} 只记录指向
     }
     """
    DIRECTED = True
    WEIGHT_ATTRIBUTE_NAME = "weight"
    DEFAULT_WEIGHT = 1

    def neighbors(self, node):
        """
        Return all nodes that are incident to the given node.
        """
        return list(self.graph_dict[node].keys())

    def add_node(self, node):
        """
        Add given node to the graph.

        @attention: While nodes can be of any type, it's strongly recommended to use only
        numbers and single-line strings as node identifiers if you intend to use write().

        @type  node: node
        @param node: Node identifier.

        """

        if (node not in self.graph_dict):
            self.graph_dict[node] = {}
        else:
            raise AdditionError("Node {0} already in digraph".format(node))

    def add_edge(self, edge):
        """
        Add an directed edge to the graph connecting two nodes.

        """
        u, v = edge
        for n in [u, v]:
            if not n in self.graph_dict:
                self.add_node(n)

        if v in self.graph_dict[u] and u in self.graph_dict[v]:
            raise AdditionError("Edge (%s, %s) already in digraph" % (u, v))
        else:
            self.graph_dict[u][v] = {}

    def del_edge(self, edge):
        """
        Remove an directed edge from the graph.

        @type  edge: tuple
        @param edge: Edge.
        """
        u, v = edge
        if v in self.graph_dict[u]:
            self.graph_dict[u].pop(v)

    def edge_attr(self, edge, key):
        u, v = edge
        return self.graph_dict[u][v].get(key)

    def set_edge_attr(self, edge, key, value):
        u, v = edge
        self.graph_dict[u][v][key] = value

    def edge_weight(self, edge):
        return self.edge_attr(edge, self.WEIGHT_ATTRIBUTE_NAME)

    def set_edge_weight(self, edge, weight=DEFAULT_WEIGHT):
        self.set_edge_attr(edge, self.WEIGHT_ATTRIBUTE_NAME, weight)
