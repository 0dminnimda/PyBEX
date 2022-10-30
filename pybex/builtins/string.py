from typing import List

from ..classes import EvalContext, Expr, Function, String
from ..interpreter import assert_args_amount
from .core import valueof


@Function.py
def bex_repr(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    return String(valueof(ctx, exprs[0]).repr())


string = [
    bex_repr,
]
