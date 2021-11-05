from typing import Any, Callable, Dict, Union
from .classes import EvalContext, Funcall, Expr, Number, Program, String, Word, Function
from dataclasses import dataclass


def eval_word(ctx: EvalContext, expr: Word) -> Any:
    variable = ctx.namespase[expr.value]
    if not isinstance(variable, Function):
        return variable
    raise TypeError(f"name {expr.value} should not be callable "
                    "because it was used as Word")


def eval_funcall(ctx: EvalContext, expr: Funcall) -> Expr:
    func = ctx.namespase[expr.func_name]
    if isinstance(func, Function):  # hasattr(obj, '__call__'):
        return func(ctx, expr.body)
    raise TypeError(f"name {expr.func_name} should be callable "
                    "because it was used in the funcall")


def eval_expr(ctx: EvalContext, expr: Expr) -> Expr:
    # if isinstance(expr, String):
    #     return expr.value
    # if isinstance(expr, Number):
    #     if isinstance(expr.value, int):
    #         return

    if isinstance(expr, Funcall):
        return eval_funcall(ctx, expr)
        # obj = ctx.namespase[expr.func_name]
        # if isinstance(obj, Function):  # hasattr(obj, '__call__'):
        #     return obj(expr.body)
        # raise TypeError(f"name of the funcall {expr.func_name} "
        #                 "should be callable")

    return expr


def interpret(ctx: EvalContext, program: Program):
    for expr in program.body:
        eval_expr(ctx, expr)
