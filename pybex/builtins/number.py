from decimal import Decimal
from typing import Any, List, Tuple, Union

from ..classes import EvalContext, Expr, Funcall, Function, Nothing, Number, String
from ..interpreter import assert_arg_type, assert_args_amount, eval_expr, eval_funcall
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
        f"or a Number, not '{type(arg1).__name__}'"
    )


def is_integer(num: Any) -> bool:
    if isinstance(num, int):
        return True
    if isinstance(num, float):
        return num.is_integer()
    return False


@Function.py
def bex_is_integer(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    arg = eval_expr(ctx, exprs[0])

    result = isinstance(arg, Number) and is_integer(arg.value)
    return Number(int(result))


def as_ratio(value: Union[int, float]) -> Tuple[int, int]:
    string = Decimal(str(value + 0.0)).to_eng_string()
    whole, _, decimal = string.rstrip("0").partition(".")
    return int(whole + decimal), 10 ** len(decimal)

    # string = str(value + .0)
    # if "e" in string:
    #     whole, _, exponent = string.partition("e")
    #     scale = max(1, 10**int(exponent))
    # else:
    #     whole, _, decimal = string.partition(".")
    #     scale = 10**len(decimal)

    # whole_digits = min(len(str(int(value))), 17)
    # decimal_digits = 17 - whole_digits
    # whole, _, decimal = f"{value:.{decimal_digits}f}".rstrip("0").partition(".")
    # return int(whole + decimal), scale


# @Function.py
# def bex_as_ratio(ctx: EvalContext, exprs: List[Expr]) -> Expr:
#     assert_args_amount(ctx, exprs, "==", 1)

#     arg = eval_expr(ctx, exprs[0])
#     arg = assert_arg_type(ctx, arg, 0, Number)

#     a, b = as_ratio(arg.value)
#     return make_list(a, b)


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
    bex_is_integer,
    bex_add,
    bex_mul,
    bex_less,
]
