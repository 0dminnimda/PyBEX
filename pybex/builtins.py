from typing import List, NoReturn

from .classes import (EvalContext, Expr, Funcall, Function, Nothing, Number,
                      Scope, String, Word)
from .interpreter import (assert_arg_type, assert_args_amount, eval_expr,
                          eval_funcall)


@Function.py
def say(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    expr: Expr

    def print_expr(expr: Expr, **kwargs):
        print(str(eval_expr(ctx, expr)), **kwargs)
        # if isinstance(expr, Word):
        #     print(eval_word(ctx, expr), **kwargs)
        # else:
        #     print(str(expr), **kwargs)

    for expr in exprs[:-1]:
        print_expr(expr, end=" ")
    for expr in exprs[-1:]:
        print_expr(expr, end="")
    print()

    return Nothing


@Function.named_py("if")
def if_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 3)
    # if len(exprs) != 3:
    #     raise ValueError("`if` expects 3 arguments")

    test = assert_arg_type(ctx, eval_expr(ctx, exprs[0]),
                           0, Number, "should evaluate to a {type.__name__}")
    # if not isinstance(test, Number):
    #     raise TypeError("first argument for `if` should evaluate to a number")

    ind = 1 + int(not test.value)  # True - 1, False - 2
    return eval_expr(ctx, exprs[ind])


@Function.py
def this(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)
    # if len(exprs) != 1:
    #     raise ValueError("`this` takes in exactly one argument")

    return exprs[0]  # we don't evaluate funcall, only return it!


@Function.named_py("type")
def type_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)
    # if len(exprs) != 1:
    #     raise ValueError("`type` takes in exactly one argument")

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
    # if len(exprs) < 2:
    #     raise ValueError("`add_args` takes in at least two argument")

    arg1 = assert_arg_type(ctx, exprs[0], 0, Funcall)
    # if not isinstance(exprs[0], Funcall):
    #     raise TypeError("first argument for `add_args` must be a funcall")

    arg1.args.extend(exprs[1:])

    return arg1


@Function.py
def valueof(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)
    # if len(exprs) != 1:
    #     raise ValueError("`valueof` takes in exactly one argument")

    value = exprs[0]
    while isinstance(value, Word):
        value = eval_expr(ctx, value)

    return value


@Function.py
def call(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, ">=", 1)
    # if len(exprs) < 1:
    #     raise ValueError("`call` takes in at least one argument")

    if isinstance(exprs[0], Funcall):
        arg1 = assert_arg_type(ctx, eval_funcall(ctx, exprs[0]), 0, Function,
                               "should evaluate to a {type.__name__}")
    else:
        arg1 = assert_arg_type(ctx, valueof(ctx, exprs[:1]), 0, Function)
    return eval_expr(ctx, arg1(ctx, exprs[1:]))

    # arg =
    # if isinstance(arg, Function):
    #     return eval_expr(ctx, arg(ctx, exprs[1:]))
    # if isinstance(arg, String):
    #     return eval_expr(ctx, Funcall(arg.value, exprs[1:]))

    # raise TypeError("first argument for `call` must be a funcall or string")


@Function.named_py("eval")
def eval_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 1)
    # if len(exprs) != 1:
    #     raise ValueError("`eval` takes in exactly one argument")

    return eval_expr(ctx, exprs[0])


@Function.py
def assign(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    assert_args_amount(ctx, exprs, "==", 2)
    # if len(exprs) != 2:
    #     raise ValueError("`assign` takes in exactly two argument")

    arg1 = assert_arg_type(ctx, exprs[0], 0, Word)
    # if not isinstance(arg1, Word):
    #     raise TypeError("first argument for `assign` must be a word")

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
    # if len(exprs) < 1:
    #     raise ValueError("`function` takes in at least one argument")

    args_func = assert_arg_type(ctx, func_body[0], 0, Funcall)
    # if not isinstance(, Funcall):
    #     raise TypeError("first argument for `function` must be a funcall")

    # args_func = assert_arg_type(ctx, eval_expr(ctx, args_func), 0, Funcall)
    # if not isinstance(args_f, Funcall):
    #     raise TypeError("first argument for `function` must be a funcall")

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

        # if len(exprs) != len(args):
        #     raise ValueError("`function` takes in at least one argument")

    return bex_func


@Function.py
def args(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    # for ind, expr in enumerate(exprs):
    #     assert_arg_type(ctx, expr, ind, Word)
    # if not isinstance(expr, Word):
    #     raise TypeError("any argument for `args` must be a word")

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
})
