from time import time
from typing import List

from ..classes import EvalContext, Expr, Function, Number
from ..interpreter import assert_args_amount


@Function.py
def bex_time(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 0)
    return Number(time())


timemodule = [
    bex_time,
]
