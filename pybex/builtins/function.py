from typing import List, NamedTuple, NoReturn, Set

from ..classes import EvalContext, Expr, Funcall, Function, Nothing, Word
from ..interpreter import assert_arg_type, assert_args_amount, eval_expr
from .core import bex_eval


class Arg(NamedTuple):
    name: str
    evaluate: bool


def make_args(ctx: EvalContext, args_func: Funcall) -> List[Arg]:
    args = []
    for ind, expr in enumerate(args_func.args):
        funcall = False
        if isinstance(expr, Funcall) and expr.name == bex_eval.name:
            assert_args_amount(ctx, expr.args, "==", 1, bex_eval.name)
            expr = expr.args[0]
            funcall = True
        args.append(Arg(assert_arg_type(ctx, expr, ind, Word).value, funcall))
    return args


@Function.py
def bex_function(ctx: EvalContext, func_body: List[Expr]) -> Expr:
    assert_args_amount(ctx, func_body, ">=", 1)

    args_func = assert_arg_type(ctx, func_body[0], 0, Funcall)
    func_args = make_args(ctx, args_func)  # validation of the args

    @Function.named_py("<unnamed_function>")
    def bex_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
        assert_args_amount(ctx, exprs, "==", len(func_args))

        # evaluate arguments before entering a new scope
        for arg, expr in zip(func_args, exprs):
            if arg.evaluate:
                expr = eval_expr(ctx, expr)
            ctx.scope.namespace[arg.name] = expr

        ctx.add_new_scope()

        result: Expr = Nothing
        for expr in func_body:
            if isinstance(expr, Funcall) and expr.name == bex_return.name:
                assert_args_amount(ctx, expr.args, "==", 1, bex_return.name)
                result = eval_expr(ctx, expr.args[0])
                break
            eval_expr(ctx, expr)

        ctx.pop_scope()

        return result

    return bex_func


@Function.py
def bex_args(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    return Funcall("args", exprs)


@Function.py
def bex_return(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    raise RuntimeError("You can 'return' only inside functions")


function = [
    bex_function,
    bex_args,
    bex_return,
]
