from decimal import Decimal
from typing import List, NamedTuple, NoReturn, Set, Tuple, Union

from ..classes import EvalContext, Expr, Funcall, Function, Nothing, Number, Word
from ..interpreter import (
    assert_arg_type,
    assert_args_amount,
    eval_expr,
    eval_funcall,
    raise_argument_error,
)
from .core import valueof
from .number import is_integer


@Function.py
def bex_range(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, ">=", 1)
    assert_args_amount(ctx, exprs, "<=", 3)

    for i, arg in enumerate(exprs):
        assert_arg_type(ctx, arg, i, Number)

    if len(exprs) == 1:
        exprs.insert(0, Number(0))
        exprs.append(Number(1))
    elif len(exprs) == 2:
        exprs.append(Number(1))
    elif len(exprs) == 3:
        pass
    else:
        raise RuntimeError(
            "Unreachable: length check didn't work, " f"got {len(exprs)} arguments"
        )

    if exprs[2] == 0:
        raise ValueError("range() arg 3 must not be zero")

    return Funcall(bex_range.name, exprs)


@Function.py
def bex_for(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, ">=", 2)

    variable = assert_arg_type(ctx, exprs[0], 0, Word).value

    iterable_arg = assert_arg_type(
        ctx,
        valueof(ctx, exprs[1]),
        1,
        Funcall,
        "must have value that is a `{type.__name__}`",
    )

    if iterable_arg.name != bex_range.name:
        raise_argument_error(
            2,
            ctx.last_funcall.name,
            f"must be a `{bex_range.name}` funcall",
            iterable_arg.name,
        )

    iterable_value = assert_arg_type(
        ctx,
        eval_funcall(ctx, iterable_arg),
        1,
        Funcall,
        "must have value that'll evaluate to a `{type.__name__}`",
    )

    start, stop, step = [
        arg.value
        for arg in iterable_value.args
        if isinstance(arg, Number)  # this line is only for typecheckers
    ]

    body = exprs[2:]
    namespace_setter = ctx.scope.namespace.__setitem__

    if is_integer(step):
        while start < stop:
            namespace_setter(variable, Number(start))
            for expr in body:
                eval_expr(ctx, expr)
            start += step
    else:
        r = str(step + 0.0)
        if "e" in r:
            step_pression = int(r.partition("-")[2])
        else:
            step_pression = len(r.partition(".")[2])
        start_pression = len(str(start).partition(".")[2])
        stop_pression = len(str(stop).partition(".")[2])

        scale = 10**step_pression
        start_scale = 10**start_pression
        stop_scale = 10**stop_pression

        start = int(start * start_scale) * int(scale / start_scale)
        stop = int(stop * stop_scale) * int(scale / stop_scale)
        step = int(step * scale)

        while start < stop:
            namespace_setter(variable, Number(start / scale))
            for expr in body:
                eval_expr(ctx, expr)
            start += step

    # XXX: remove variable in the end of the loop?
    # del ctx.scope.namespace[variable]
    return Nothing

    # iterable_value = valueof(ctx, exprs[1:2])
    # if isinstance(iterable_value, Funcall):
    #     iterable = iter(iterable_value.args)

    #     def next_():
    #         try:
    #             return next(iterable)
    #         except StopIteration:
    #             return Nothing
    # else:
    #     iterable_value = assert_arg_type(ctx, iterable_value, 1, Function)

    #     def next_():
    #         return iterable_value(ctx, [])

    # while 1:
    #     value: Expr = next_()
    #     if value is Nothing:
    #         # remove variable in the end of the loop?
    #         # del ctx.scope.namespace[variable]
    #         return Nothing

    #     ctx.scope.namespace[variable] = value
    #     bex_exec(ctx, exprs[2:])

    # raise RuntimeError("Unreachable: end of the for loop "
    #                    "without getting Nothing from function")


loop = [
    bex_range,
    bex_for,
]
