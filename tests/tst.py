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


@Function.py
def bex_range(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, ">=", 1)
    assert_args_amount(ctx, exprs, "<=", 3)

    for i, arg in enumerate(exprs):
        assert_arg_type(ctx, arg, i, Number)

    if len(exprs) == 1:
        # exprs = [Number(0), *exprs, Number(1)]
        exprs.insert(0, Number(0))
        exprs.append(Number(1))
    elif len(exprs) == 2:
        exprs.append(Number(1))
    elif len(exprs) == 3:
        pass
    else:
        raise RuntimeError("Unreachable: length check didn't work, "
                           f"got {len(exprs)} arguments")

    if exprs[2] == 0:
        raise ValueError("range() arg 3 must not be zero")

    return Funcall("range", exprs)


def is_integer(num: Any) -> bool:
    if isinstance(num, int):
        return True
    if isinstance(num, float):
        return num.is_integer()
    return False


@Function.py
def bex_is_integer(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    arg = exprs[0]
    if isinstance(arg, Number):
        return Number(int(is_integer(arg.value)))

    return Number(0)


from math import fsum
# from decimal import decimal


@Function.py
def bex_for(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, ">=", 2)

    variable = assert_arg_type(ctx, exprs[0], 0, Word).value

    iterable_arg = assert_arg_type(
        ctx, valueof(ctx, exprs[1]), 1, Funcall,
        "must have value that is a `{type.__name__}`")

    if iterable_arg.name != bex_range.name:
        raise_argument_error(
            2, ctx.last_funcall.name,
            f"must be a `{bex_range.name}` funcall",
            iterable_arg.name)

    iterable_value = assert_arg_type(
        ctx, eval_funcall(ctx, iterable_arg), 1,
        Funcall, "must have value that'll "
        "evaluate to a `{type.__name__}`")

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
            bex_exec(ctx, body)
            start += step
    else:
        step += .0


        # diff = round(
        #     stop - start, max(
        #         len(str(stop).split(".")[1]),
        #         len(str(start).split(".")[1])
        #     )
        # )
        r = str(step)
        if "e" in r:
            step_pression = int(r.split("-")[1])
        else:
            step_pression = len(r.split(".")[1])
        start_pression = len(str(start).split(".")[1])
        stop_pression = len(str(stop).split(".")[1])

        scale = 10**step_pression
        start_scale = 10**start_pression
        stop_scale = 10**stop_pression

        start = int(start * start_scale) * int(scale / start_scale)
        stop = int(stop * stop_scale) * int(scale / stop_scale)
        step = int(step * scale)

        while start < stop:
            namespace_setter(variable, Number(start / scale))
            bex_exec(ctx, body)
            start += step
            # print(start)

        # pression = 15 - len(str(int(stop)))
        # # len(str(step).split(".")[1]) + len(str(int(start)))
        # while start < stop:
        #     namespace_setter(variable, Number(start))
        #     bex_exec(ctx, body)
        #     start = round(step + start, pression)

        # i = 0
        # num = start
        # while num < stop:
        #     namespace_setter(variable, Number(num))
        #     bex_exec(ctx, body)
        #     i += 1
        #     num = start + step * i

        # while start < stop:
        #     namespace_setter(variable, Number(start))
        #     bex_exec(ctx, body)
        #     start = fsum((start, step))

        # delta = stop - start
        # fstep = delta / num
        # for i in range(num):
        #     ctx.scope.namespace[variable] = Number(
        #         fsum((start, i * )))
        #     bex_exec(ctx, exprs[2:])

        # i = 0
        # num = start
        # while num < stop:
        #     ctx.scope.namespace[variable] = Number(num)
        #     bex_exec(ctx, exprs[2:])
        #     i += 1
        #     num = start + step * i
        #     print(i, num, start, step * i)

        # nm1 = n - 1
        # nm1inv = 1.0 / nm1
        # s = start*nm1
        # for i in range(n):
        #     yield nm1inv * (s - (start + stop)*i)

    # remove variable in the end of the loop?
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


ctx = EvalContext(Scope.from_funcions(
    # my_func,
    # my_func2,
    bex_range,
    bex_is_integer,
    bex_for,
))

# interpret(parse_source(program_body), ctx)

run_interactive_mode(ctx)


breakpoint
