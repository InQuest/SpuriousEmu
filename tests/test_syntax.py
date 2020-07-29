from collections import deque
from typing import Tuple, Dict, Any

import networkx as nx
import matplotlib

from emu import syntax
from tests.test import (assert_correct_function, SourceFile, Result)
from tests.test import run_function, export_result


def parsing(vbs: SourceFile) -> Result:
    ast = syntax.parse_file(vbs)
    return ast.to_dict()


def parsing_show(vbs: SourceFile) -> Result:
    ast = syntax.parse_file(vbs)
    display_digraph(*build_digraph_from_ast(ast))


def build_digraph_from_ast(ast: syntax.AST) \
        -> Tuple[nx.DiGraph, Dict[Any, str]]:
    graph = nx.DiGraph()

    nodes = deque([ast])
    labels = dict()
    while len(nodes) != 0:
        current_node = nodes.pop()
        graph.add_node(current_node)
        labels[current_node] = type(current_node).__name__
        children = []

        for attr_name in dir(current_node):
            if attr_name.startswith("_"):
                continue
            attr = getattr(current_node, attr_name)

            if isinstance(attr, syntax.AST):
                children.append(attr)

            elif isinstance(attr, (list, tuple)):
                children.extend(attr)

        for child in children:
            graph.add_edge(current_node, child)
            nodes.append(child)

    return graph, labels


def display_digraph(graph: nx.DiGraph, labels: Dict[Any, str]) -> None:
    pos = nx.drawing.nx_pydot.graphviz_layout(graph, prog="dot")
    nx.draw(graph, pos, labels=labels)
    matplotlib.pyplot.show()


def test_expressions():
    export_result("syntax_expression", parsing)


def test_inline_declarations():
    export_result("syntax_inline_declaration", parsing)


def test_loops_conditionals():
    export_result("syntax_loop_conditional", parsing)


def test_function_definitions():
    run_function("syntax_function_definition", parsing_show)


# def test_types():
#     run_function("types", parsing)
