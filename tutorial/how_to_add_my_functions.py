from pybex import EvalContext, Scope, interpret, parse_source
from pybex.classes import Function

program_body = """bex code"""


@Function.py  # my_func.name == "my_func"
def my_func(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    ...  # do stuff


@Function.named_py("gg")  # my_func2.name == "gg"
def my_func2(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    ...  # do stuff


ctx = EvalContext(Scope({
    my_func.name: my_func,
    my_func2.name: my_func2,
}))

interpret(parse_source(program_body), ctx)
