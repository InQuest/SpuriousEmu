from emu import syntax
from tests.test import (assert_correct_function, SourceFile, Result)
from tests.test import run_function


def parsing(vbs: SourceFile) -> Result:
    ast = syntax.parse_file(vbs)
    return ast.to_dict()


def test_expressions():
    assert_correct_function("basic_01", parsing)


def test_inline_declarations():
    assert_correct_function("basic_02", parsing)


def test_loops():
    assert_correct_function("basic_03", parsing)


def test_conditionals():
    assert_correct_function("basic_04", parsing)


def test_function_definitions():
    assert_correct_function("basic_05", parsing)


def test_types():
    assert_correct_function("types", parsing)
