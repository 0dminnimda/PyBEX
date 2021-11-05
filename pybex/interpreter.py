from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from .classes import EvalContext, Funcall, Expr, Nothing, Number, Program, String, Unfinished, Word, Function
from .parser import parse_source
from . import __version__
from dataclasses import dataclass
import traceback
import sys


def eval_word(ctx: EvalContext, expr: Word) -> Any:
    return ctx.namespase[expr.value]
    # variable = ctx.namespase[expr.value]
    # if not isinstance(variable, Function):
    #     return variable
    # raise TypeError(f"name {expr.value} should not be callable "
    #                 "because it was used as Word")


def eval_funcall(ctx: EvalContext, expr: Funcall) -> Expr:
    func = ctx.namespase[expr.name]
    if isinstance(func, Function):  # hasattr(obj, '__call__'):
        return func(ctx, expr.args)
    raise TypeError(f"name {expr.name!r} should be callable "
                    "because it was used in the funcall")


def eval_expr(ctx: EvalContext, expr: Expr) -> Expr:
    if isinstance(expr, Funcall):
        return eval_funcall(ctx, expr)
    if isinstance(expr, Word):
        return eval_word(ctx, expr)
    return expr


def interpret(ctx: EvalContext, program: Program):
    for expr in program.body:
        eval_expr(ctx, expr)


def make_traceback_string() -> str:
    return "".join(traceback.format_exception(*sys.exc_info()))
    # sys.last_type, sys.last_value, last_tb = ei = sys.exc_info()
    # sys.last_traceback = last_tb
    # try:
    #     return "".join(traceback.format_exception(
    #         ei[0], ei[1], last_tb.tb_next))
    # finally:
    #     del last_tb, ei


def run_interactive_mode(ctx: EvalContext, banner: Optional[str] = None,
                         prompts: Tuple[str, str] = ("bex> ",
                                                     " ... "),
                         write: Callable[[str], Any] = sys.stderr.write):
    if banner is None:
        write(f"Welcome to PyBEX {__version__}"
              f" interactive mode on {sys.platform}! :)\n")
    else:
        write(banner)

    buffer: List[str] = []
    more: int = 0
    while 1:
        try:
            line = input(prompts[more])
        except EOFError:
            write("\n")
            break
        except KeyboardInterrupt:
            write("\nKeyboardInterrupt\n")
            buffer.clear()
            more = 0
            continue

        buffer.append(line)
        exprs = parse_source("\n".join(buffer), "single").body

        if len(exprs) == 0:
            continue

        assert len(exprs) == 1
        try:
            result = eval_expr(ctx, exprs[0])
        except SystemExit:
            raise
        except:  # noqa
            write(make_traceback_string())
            buffer.clear()
            more = 0  # XXX: is possible to be 1?
            continue

        if result is Unfinished:
            more = 1
            continue

        buffer.clear()
        more = 0
        if result is not Nothing:
            write(repr(result) + "\n")
