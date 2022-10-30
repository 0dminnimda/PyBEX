import sys
import traceback
from typing import Any, Callable, List, Optional, Tuple

from lark.exceptions import LarkError

from . import __version__
from .builtins import builtin_scope
from .classes import EvalContext, Nothing, Program, Unfinished
from .interpreter import eval_expr
from .parser import parse_source


def make_ctx_with_builtins(ctx: EvalContext) -> EvalContext:
    new_ctx = EvalContext()
    new_ctx.scope.update_by_scope(builtin_scope)
    new_ctx.scope.update_by_scope(ctx.scope)
    return new_ctx


def interpret(program: Program, ctx: EvalContext = EvalContext()):
    ctx = make_ctx_with_builtins(ctx)
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


def run_interactive_mode(ctx: EvalContext = EvalContext(),
                         banner: Optional[str] = None,
                         prompts: Tuple[str, str] = ("bex> ",
                                                     " ... "),
                         write: Callable[[str], Any] = sys.stderr.write):
    ctx = make_ctx_with_builtins(ctx)

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
        try:
            exprs = parse_source("\n".join(buffer), "single").body
        except LarkError:
            # XXX: SyntaxError
            write(make_traceback_string())
            buffer.clear()
            more = 0  # XXX: is possible to be 1?
            continue

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
            write(result.repr() + "\n")
