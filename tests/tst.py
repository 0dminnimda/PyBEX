from typing import Any, List

from pybex import EvalContext, Scope, interpret, parse_source
from pybex.builtins import bex_exec, valueof
from pybex.classes import Expr, Funcall, Function, Nothing, Number, Word
from pybex.interpreter import (assert_arg_type, assert_args_amount, eval_expr,
                               eval_funcall, raise_argument_error)
from pybex.run import run_interactive_mode

# print(result)

program_body = '''
say("""long
word""",
"and multiline func")
say("Hello", "world!")
say("I am", name, "!")

"""dfgdfg5675"""

56456
45645.4546
1_000_000

say(if(1, 6, 8))  # 6
say(this(say()))  # Funcall(name='say', args=[])

say(this(say(pi, 31415, this(), if)))
# Funcall(name='say', args=[
#     Word(value='pi'), 31415,
#     Funcall(name='this', args=[]), Word(value='if')])

'''


# @Function.py  # my_func.name == "my_func"
# def bex_my_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
#     # do stuff


# @Function.named_py("gg")  # my_func2.name == "gg"
# def my_func2(ctx: EvalContext, exprs: List[Expr]) -> Expr:
#     # do stuff


def self_returning(name=None):
    def inner(func):
        nonlocal name
        if name is None:
            name = func.__name__

        @Function.named_py(name)
        def wrapper(ctx: EvalContext, exprs: List[Expr]) -> Expr:
            func(ctx, exprs)
            return Funcall(name, exprs)

        return wrapper
    return inner

ctx = EvalContext(Scope.from_funcions(
    # my_func,
    # my_func2,
))

# interpret(parse_source(program_body), ctx)

run_interactive_mode(ctx)


breakpoint
