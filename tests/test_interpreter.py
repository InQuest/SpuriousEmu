from emu import Parser, interpreter, Compiler, reference
from tests.test import (assert_correct_function, SourceFile, Result)

from tests.test import run_function


def interpreting(vbs: SourceFile) -> Result:
    ast = Parser.parse_file(vbs)
    comp = Compiler()
    comp.add_module(ast, reference.ProceduralModule, "main_module")
    comp.load_host_project("./emu/VBA")

    interp = interpreter.Interpreter(comp.program)
    interp.run("Main")

    return interp._outside_world.to_dict()


def evaluate_expressions(vbs: SourceFile) -> Result:
    ast = Parser.parse_file(vbs)
    interp = interpreter.Interpreter()
    expressions = []
    for expression in ast.body:
        expressions.append(str(interp.evaluate(expression)))
    return {'expressions': expressions}


def test_type():
    assert_correct_function("interpreter_type", evaluate_expressions)


def test_literal_expression():
    assert_correct_function('interpreter_literal_expression',
                            evaluate_expressions)


def test_draf():
    run_function('interpreter_01', interpreting)


def test_draft():
    run_function("draft", interpreting)
