from typing import List

from ..classes import (EvalContext, Expr, Funcall, Function, Nothing, Number,
                       String)
from ..interpreter import (assert_arg_type, assert_args_amount, eval_expr,
                           eval_funcall)
from .core import valueof


@Function.py
def bex_int(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    arg1 = exprs[0]
    if isinstance(arg1, Funcall):
        arg1 = eval_funcall(ctx, arg1)

    arg1 = valueof(ctx, arg1)

    if isinstance(arg1, (String, Number)):
        return Number(int(arg1.value))
    if arg1 is Nothing:
        return Number(0)

    raise TypeError(
        "int() argument must be a String, Nothing "
        f"or a Number, not '{type(arg1).__name__}'")


@Function.py
def bex_add(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 2)

    o1 = eval_expr(ctx, exprs[0])
    o1 = assert_arg_type(ctx, o1, 0, Number)

    o2 = eval_expr(ctx, exprs[1])
    o2 = assert_arg_type(ctx, o2, 1, Number)

    return Number(o1.value + o2.value)


@Function.py
def bex_mul(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 2)

    o1 = eval_expr(ctx, exprs[0])
    o1 = assert_arg_type(ctx, o1, 0, Number)

    o2 = eval_expr(ctx, exprs[1])
    o2 = assert_arg_type(ctx, o2, 1, Number)

    return Number(o1.value * o2.value)


@Function.py
def bex_less(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 2)

    o1 = eval_expr(ctx, exprs[0])
    o1 = assert_arg_type(ctx, o1, 0, Number)

    o2 = eval_expr(ctx, exprs[1])
    o2 = assert_arg_type(ctx, o2, 1, Number)

    return Number(o1.value < o2.value)


number = [
    bex_int,
    bex_add,
    bex_mul,
    bex_less
]
