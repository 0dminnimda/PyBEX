from typing import Any, List
from pybex.parser import parse_source
from pybex.interpreter import interpret, eval_word, eval_expr
from pybex.classes import Function, Expr, Nothing, Number, String, EvalContext, Word


def to_string(expr: Expr) -> str:
    if isinstance(expr, String):
        return expr.value
    if isinstance(expr, Number):
        return str(expr.value)
    if isinstance(expr, Nothing):
        return "Nothing"

    raise TypeError(f"expr of type {type(expr)} cannot be converted to string")


@Function
def say(ctx: EvalContext, exprs: List[Expr]) -> Expr:
    expr: Expr

    def print_expr(expr: Expr, **kwargs):
        if isinstance(expr, Word):
            print(eval_word(ctx, expr), **kwargs)
        else:
            print(to_string(expr), **kwargs)

    for expr in exprs[:-1]:
        print_expr(expr, end=" ")
    for expr in exprs[-1:]:
        print_expr(expr, end="")
    print()

    return Nothing()


ctx = EvalContext({
    "say": say,
    "name": "Alex"
})


# print(result)

program_body = '''
say("""long
word""")
say("Hello", "world!")
say("I am", name, "!")
'''

# interpret(parse_source(program_body), ctx)

while 1:
    r = eval_expr(ctx, parse_source(input("bex >>> ")).body[0])
    if not isinstance(r, Nothing):
        print(to_string(r))

breakpoint
