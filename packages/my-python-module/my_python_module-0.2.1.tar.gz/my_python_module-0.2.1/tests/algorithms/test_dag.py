#!/usr/bin/env python
# -*-coding:utf-8-*-


from my_python_module.algorithms.graph.dag import DAG, CyclicError
import logging
logging.basicConfig(level=logging.DEBUG)

import pytest

def test_dag():
    dag = DAG()
    dag.add_edge(('a', 'b'))
    dag.add_edge(('a', 'c'))
    dag.add_edge(('b', 'e'))
    dag.add_edge(('e', 'f'))
    dag.add_edge(('f', 'c'))
    dag.add_edge(('c', 'g'))
    dag.add_edge(('g', 'h'))

    assert dag.sort()

    with pytest.raises(CyclicError):
        dag.add_edge(('g','a'))

    print(dag)