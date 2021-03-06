from typing import Any, List, Optional, Type, TypeVar, NoReturn

from .classes import EvalContext, Expr, Funcall, Function, Word

# import warnings
# def num_of_args_to_word(number: int) -> str:
#     assert number >= 0
#     words = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
#              6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
#              11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
#              15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
#              19: 'nineteen', 20: 'twenty'}

#     if number < 21:
#         return words[number]
#     else:
#         warnings.warn("PyBEX don't support crazy functions "
#                       "with more than 20 arguments")
#         return "too many (over 20)"


T = TypeVar("T")


def assert_args_amount(ctx: EvalContext, args: List[Expr],
                       action: str, amount: int) -> None:
    assert isinstance(ctx.last_funcall, Funcall)

    if action == "==":
        if len(args) != amount:
            raise ValueError(f"`{ctx.last_funcall.name}` takes in exactly "
                             f"{amount} argument(s) but provided {len(args)}")
    elif action == ">=":
        if len(args) < amount:
            raise ValueError(f"`{ctx.last_funcall.name}` takes in at least "
                             f"{amount} argument(s) but provided {len(args)}")
    elif action == "<=":
        if len(args) > amount:
            raise ValueError(f"`{ctx.last_funcall.name}` takes in at most "
                             f"{amount} argument(s) but provided {len(args)}")
    else:
        raise ValueError(f"Unknown `action`: {action}")


def raise_argument_error(number: int, funcname: str,
                         message: str, found: str) -> NoReturn:
    raise TypeError(
        f"argument number {number} for "
        f"`{funcname}` {message}"
        f" but found `{found}`")
    # f"must be a {type.__name__}")


def assert_arg_type(ctx: EvalContext, arg: Expr,
                    ind: int, type_: Type[T],
                    txt: Optional[str] = None) -> T:
    assert isinstance(ctx.last_funcall, Funcall)

    if txt is None:
        txt = "must be a `{type.__name__}`"

    if not isinstance(arg, type_):
        raise_argument_error(
            ind + 1,
            ctx.last_funcall.name,
            txt.format(type=type_),
            type(arg).__name__)

    return arg  # so type checkers can be work properly


def get_name(ctx: EvalContext, name: str) -> Expr:
    for scope in ctx.scopes[::-1]:
        try:
            return scope.namespace[name]
        except KeyError:
            continue

    raise NameError(f"name {name!r} is not defined")


def eval_word(ctx: EvalContext, expr: Word) -> Any:
    return get_name(ctx, expr.value)

    # try:
    #     return ctx.scope.namespace[expr.value]
    # except KeyError:
    #     raise NameError(f"name {expr.value!r} is not defined") from None

    # variable = ctx.namespase[expr.value]
    # if not isinstance(variable, Function):
    #     return variable
    # raise TypeError(f"name {expr.value} should not be callable "
    #                 "because it was used as Word")


def eval_funcall(ctx: EvalContext, expr: Funcall) -> Expr:
    func = get_name(ctx, expr.name)
    # func = assert_arg_type(ctx, get_name(ctx, expr.name), )

    if not isinstance(func, Function):
        raise TypeError(f"name {expr.name!r} in Funcall should be a Function "
                        f"but found {type(func).__name__}")
        # hasattr(obj, '__call__'):
        # raise TypeError(f"name {expr.name!r} should be callable "
        #                 "because it was used in the funcall")

    # for ind, arg in enumerate(expr.args):
    #     if isinstance(arg, Funcall) and arg.name == "eval":
    #         expr.args[ind] = eval_funcall(ctx, arg)

    prev_funcall = ctx.last_funcall
    ctx.last_funcall = expr
    try:
        return func(ctx, expr.args)
    finally:
        ctx.last_funcall = prev_funcall


def eval_expr(ctx: EvalContext, expr: Expr) -> Expr:
    if isinstance(expr, Funcall):
        return eval_funcall(ctx, expr)
    if isinstance(expr, Word):
        return eval_word(ctx, expr)
    return expr
