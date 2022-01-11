from typing import List, NoReturn, Set

from .classes import (EvalContext, Expr, Funcall, Function, Nothing, Number,
                      Scope, String, Word)
from .interpreter import (assert_arg_type, assert_args_amount, eval_expr,
                          eval_funcall, raise_argument_error)


@Function.py
def bex_say(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    expr: Expr

    def print_expr(expr: Expr, **kwargs):
        print(str(eval_expr(ctx, expr)), **kwargs)

    for expr in exprs[:-1]:
        print_expr(expr, end=" ")
    for expr in exprs[-1:]:
        print_expr(expr, end="")
    print()

    return Nothing


@Function.py
def bex_if(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 3)

    test = assert_arg_type(ctx, eval_expr(ctx, exprs[0]),
                           0, Number, "should evaluate to a `{type.__name__}`")

    ind = 1 + int(not test.value)  # True - 1, False - 2
    return eval_expr(ctx, exprs[ind])


@Function.py
def bex_this(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    return exprs[0]


@Function.py
def bex_type(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    return String(type(exprs[0]).__name__)


# @Function.py
# def bex_list(ctx: EvalContext, exprs: List[Expr]) -> Expr:
#     return Funcall("list", exprs)


@Function.py
def bex_noeval(ctx: EvalContext, exprs: List[Expr]) -> NoReturn:
    raise RuntimeError("`noeval` funcall should not be evaluated")


@Function.py
def bex_add_args(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, ">=", 2)

    arg1 = assert_arg_type(ctx, exprs[0], 0, Funcall)
    arg1.args.extend(exprs[1:])

    return arg1


def valueof(ctx: EvalContext, value: Expr) -> Expr:
    cache: Set[str] = set()
    while isinstance(value, Word):
        if value.value in cache:
            raise RecursionError("`valueof` encountered a reference cycle "
                                 f"consisting of {cache}")
        cache.add(value.value)
        value = eval_expr(ctx, value)

    return value


@Function.py
def bex_valueof(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)
    return valueof(ctx, exprs[0])


@Function.py
def bex_call(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, ">=", 1)

    if isinstance(exprs[0], Funcall):
        arg1 = assert_arg_type(ctx, eval_funcall(ctx, exprs[0]), 0, Function,
                               "should evaluate to a '{type.__name__}'")
    else:
        arg1 = assert_arg_type(ctx, valueof(ctx, exprs[0]), 0, Function)
    return arg1(ctx, exprs[1:])


@Function.py
def bex_eval(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    return eval_expr(ctx, exprs[0])


@Function.py
def bex_assign(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 2)
    arg1 = assert_arg_type(ctx, exprs[0], 0, Word)

    arg2 = exprs[1]
    if isinstance(arg2, Funcall):
        arg2 = eval_funcall(ctx, arg2)

    ctx.scope.namespace[arg1.value] = arg2
    if isinstance(arg2, Function):
        arg2.name = arg1.value
    return arg2


@Function.py
def bex_function(ctx: EvalContext, func_body: List[Expr]) -> Expr:
    assert_args_amount(ctx, func_body, ">=", 1)

    args_func = assert_arg_type(ctx, func_body[0], 0, Funcall)
    # validation of the args
    func_args = [assert_arg_type(ctx, expr, ind, Word)
                 for ind, expr in enumerate(args_func.args)]

    @Function.named_py("<unnamed_function>")
    def bex_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
        assert_args_amount(ctx, exprs, "==", len(func_args))

        ctx.add_new_scope()

        for word, expr in zip(func_args, exprs):
            ctx.scope.namespace[word.value] = expr

        for expr in func_body:
            eval_expr(ctx, expr)  # use return when Return_s will be supported

        ctx.pop_scope()

        return Nothing
    return bex_func


@Function.py
def bex_args(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    return Funcall("args", exprs)


@Function.py
def bex_exec(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    for expr in exprs:
        eval_expr(ctx, expr)

    return Nothing


@Function.py
def bex_input(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "<=", 1)

    prompt = ""
    for expr in exprs:
        prompt = assert_arg_type(ctx, expr, 0, String).value

    return String(input(prompt))


@Function.py
def bex_repr(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    return String(repr(valueof(ctx, exprs[0])))


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
        f"or a Number, not '{type(arg1).__name__}'")


@Function.py
def bex_add(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 2)

    o1 = exprs[0]
    if isinstance(o1, Number):
        o2 = assert_arg_type(ctx, exprs[1], 1, Number)
        return Number(o1.value + o2.value)
    else:
        raise_argument_error(
            1,
            ctx.last_funcall.name,
            f"must be a `{Number.__name__}`",
            type(o1).__name__)


builtin_scope = Scope.from_funcions(
    bex_add,

    bex_say,
    bex_if,
    bex_this,
    bex_type,
    # bex_noeval,  # do we really need it?
    bex_add_args,
    bex_valueof,
    bex_call,
    bex_eval,
    bex_assign,
    bex_function,
    bex_args,
    bex_exec,
    bex_input,
    bex_repr,
    bex_int,
)
