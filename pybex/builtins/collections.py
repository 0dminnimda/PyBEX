from typing import List

from ..classes import EvalContext, Expr, Funcall, Function
from ..interpreter import assert_arg_type, assert_args_amount

# @Function.py
# def bex_list(ctx: EvalContext, exprs: List[Expr]) -> Expr:
#     return Funcall("list", exprs)


@Function.py
def bex_add_args(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, ">=", 2)

    arg1 = assert_arg_type(ctx, exprs[0], 0, Funcall)
    arg1.args.extend(exprs[1:])

    return arg1


collections = [
    bex_add_args,
]
