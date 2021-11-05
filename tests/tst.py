from typing import Any, List
from pybex.parser import parse_source
from pybex.interpreter import interpret, eval_expr, run_interactive_mode
from pybex.classes import Funcall, Function, Expr, Nothing, Number, String, EvalContext, Unfinished, Word
import sys
import traceback


@Function.py
def say(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    expr: Expr

    def print_expr(expr: Expr, **kwargs):
        print(str(eval_expr(ctx, expr)), **kwargs)
        # if isinstance(expr, Word):
        #     print(eval_word(ctx, expr), **kwargs)
        # else:
        #     print(str(expr), **kwargs)

    for expr in exprs[:-1]:
        print_expr(expr, end=" ")
    for expr in exprs[-1:]:
        print_expr(expr, end="")
    print()

    return Nothing


@Function.named_py("if")
def if_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    if len(exprs) != 3:
        raise ValueError("`if` expects 3 arguments")

    test = eval_expr(ctx, exprs[0])
    if not isinstance(test, Number):
        raise TypeError("first argument for `if` should evaluate to a number")

    ind = 1 + int(not test.value)  # True - 1, False - 2
    return eval_expr(ctx, exprs[ind])


# @Function
# def define(ctx: EvalContext, exprs: List[Expr]) -> Expr:
#     if len(exprs) == 2:
#         if isinstance(exprs[0], S)
#         ctx.namespase[]


@Function.py
def this(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    if len(exprs) != 1:
        raise ValueError("`this` takes in exactly one argument")

    if not isinstance(exprs[0], Funcall):
        raise TypeError("first argument for `this` must be a function")

    return exprs[0]  # we don't evaluate funcall, only return it!


ctx = EvalContext({
    say.name: say,
    if_func.name: if_func,
    this.name: this,
    "name": "Alex"
})


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

# interpret(ctx, parse_source(program_body))

run_interactive_mode(ctx)


breakpoint
