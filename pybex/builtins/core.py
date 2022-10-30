from typing import List, NamedTuple, NoReturn, Set

from ..classes import EvalContext, Expr, Funcall, Function, Nothing, Word
from ..interpreter import (assert_arg_type, assert_args_amount, eval_expr,
                           eval_funcall)


@Function.py
def bex_eval(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    return eval_expr(ctx, exprs[0])


def valueof(ctx: EvalContext, value: Expr) -> Expr:
    cache: Set[str] = set()
    while isinstance(value, Word):
        if value.value in cache:
            raise RecursionError("`valueof` encountered a reference cycle "
                                 f"consisting of {cache}")
        cache.add(value.value)
        value = eval_expr(ctx, value)

    return value


@Function.py
def bex_valueof(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)
    return valueof(ctx, exprs[0])


@Function.py
def bex_assign(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 2)
    arg1 = assert_arg_type(ctx, exprs[0], 0, Word)

    arg2 = exprs[1]
    if isinstance(arg2, Funcall):
        arg2 = eval_funcall(ctx, arg2)

    ctx.scope.namespace[arg1.value] = arg2
    if isinstance(arg2, Function):
        arg2.name = arg1.value
    return arg2


@Function.py
def bex_exec(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    for expr in exprs:
        eval_expr(ctx, expr)

    return Nothing


@Function.py
def bex_call(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, ">=", 1)

    if isinstance(exprs[0], Funcall):
        arg1 = assert_arg_type(ctx, eval_funcall(ctx, exprs[0]), 0, Function,
                               "should evaluate to a '{type.__name__}'")
    else:
        arg1 = assert_arg_type(ctx, valueof(ctx, exprs[0]), 0, Function)
    return arg1(ctx, exprs[1:])


@Function.py
def bex_this(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    return exprs[0]


@Function.py
def bex_noeval(ctx: EvalContext, exprs: List[Expr]) -> NoReturn:
    raise RuntimeError("`noeval` funcall should not be evaluated")


core = [
    # language is build around those
    bex_eval,
    bex_valueof,
    bex_assign,
    # those are still indispensable, but more situational
    bex_exec,
    bex_call,
    bex_this,
    # bex_noeval,  # do we really need it?
]
