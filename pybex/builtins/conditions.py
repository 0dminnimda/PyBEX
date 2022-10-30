from typing import List

from ..classes import EvalContext, Expr, Function, Nothing, Number
from ..interpreter import assert_arg_type, assert_args_amount, eval_expr


@Function.py
def bex_if(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, ">=", 2)
    assert_args_amount(ctx, exprs, "<=", 3)

    test = assert_arg_type(ctx, eval_expr(ctx, exprs[0]),
                           0, Number, "should evaluate to a `{type.__name__}`")

    if test.value:
        return eval_expr(ctx, exprs[1])

    if len(exprs) == 3:
        return eval_expr(ctx, exprs[2])

    return Nothing


conditions = [
    bex_if,
]
