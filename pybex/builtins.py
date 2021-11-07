from typing import List, NoReturn, Set

from .classes import (EvalContext, Expr, Funcall, Function, Nothing, Number,
                      Scope, String, Word)
from .interpreter import (assert_arg_type, assert_args_amount, eval_expr,
                          eval_funcall)


@Function.py
def say(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    expr: Expr

    def print_expr(expr: Expr, **kwargs):
        print(str(eval_expr(ctx, expr)), **kwargs)

    for expr in exprs[:-1]:
        print_expr(expr, end=" ")
    for expr in exprs[-1:]:
        print_expr(expr, end="")
    print()

    return Nothing


@Function.named_py("if")
def if_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 3)

    test = assert_arg_type(ctx, eval_expr(ctx, exprs[0]),
                           0, Number, "should evaluate to a '{type.__name__}'")

    ind = 1 + int(not test.value)  # True - 1, False - 2
    return eval_expr(ctx, exprs[ind])


@Function.py
def this(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    return exprs[0]


@Function.named_py("type")
def type_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    return String(type(exprs[0]).__name__)


# @Function.named_py("list")
# def list_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
#     return Funcall("list", exprs)


@Function.py
def noeval(ctx: EvalContext, exprs: List[Expr]) -> NoReturn:
    raise RuntimeError("`noeval` funcall should not be evaluated")


@Function.py
def add_args(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, ">=", 2)

    arg1 = assert_arg_type(ctx, exprs[0], 0, Funcall)
    arg1.args.extend(exprs[1:])

    return arg1


@Function.py
def valueof(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    cache: Set[str] = set()
    value = exprs[0]
    while isinstance(value, Word):
        if value.value in cache:
            raise RecursionError("`valueof` encountered a reference cycle "
                                 f"consisting of {cache}")
        cache.add(value.value)
        value = eval_expr(ctx, value)

    return value


@Function.py
def call(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, ">=", 1)

    if isinstance(exprs[0], Funcall):
        arg1 = assert_arg_type(ctx, eval_funcall(ctx, exprs[0]), 0, Function,
                               "should evaluate to a '{type.__name__}'")
    else:
        arg1 = assert_arg_type(ctx, valueof(ctx, exprs[:1]), 0, Function)
    return eval_expr(ctx, arg1(ctx, exprs[1:]))


@Function.named_py("eval")
def eval_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    return eval_expr(ctx, exprs[0])


@Function.py
def assign(ctx: EvalContext, exprs: List[Expr]) -> Expr:
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
def function(ctx: EvalContext, func_body: List[Expr]) -> Expr:
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
def args(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    return Funcall("args", exprs)


@Function.named_py("exec")
def exec_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    for expr in exprs:
        eval_expr(ctx, expr)

    return Nothing


@Function.named_py("input")
def input_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "<=", 1)

    prompt = ""
    for expr in exprs:
        prompt = assert_arg_type(ctx, expr, 0, String).value

    return String(input(prompt))


@Function.named_py("repr")
def repr_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    return String(repr(exprs[0]))


@Function.named_py("int")
def int_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)

    arg1 = exprs[0]
    if isinstance(arg1, Funcall):
        arg1 = eval_funcall(ctx, arg1)

    arg1 = valueof(ctx, [arg1])

    if isinstance(arg1, (String, Number)):
        return Number(int(arg1.value))
    if arg1 is Nothing:
        return Number(0)

    raise TypeError(
        "int() argument must be a String, Nothing "
        f"or a Number, not '{type(arg1).__name__}'")


builtin_scope = Scope({
    say.name: say,
    if_func.name: if_func,
    this.name: this,
    type_func.name: type_func,
    # noeval.name: noeval,  # do we really need it?
    add_args.name: add_args,
    valueof.name: valueof,
    call.name: call,
    eval_func.name: eval_func,
    assign.name: assign,
    function.name: function,
    args.name: args,
    exec_func.name: exec_func,
    input_func.name: input_func,
    repr_func.name: repr_func,
    int_func.name: int_func,
})
