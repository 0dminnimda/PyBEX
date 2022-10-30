from typing import List

from ..classes import EvalContext, Expr, Function, Nothing, String
from ..interpreter import assert_arg_type, assert_args_amount, eval_expr


@Function.py
def bex_input(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "<=", 1)

    prompt = ""
    for expr in exprs:
        prompt = assert_arg_type(ctx, expr, 0, String).value

    return String(input(prompt))


@Function.py
def bex_say(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    expr: Expr

    print(*(eval_expr(ctx, expr).str() for expr in exprs))

    return Nothing


inout = [
    bex_input,
    bex_say,
]
