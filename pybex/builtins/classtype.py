from typing import List

from ..classes import EvalContext, Expr, Function, String
from ..interpreter import assert_args_amount


@Function.py
def bex_type(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    return String(type(exprs[0]).__name__)


classtype = [
    bex_type,
]
