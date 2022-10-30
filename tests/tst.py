from pathlib import Path

import pybex as bex

program_body = Path("tests/some_things.bex").read_text()

# def self_returning(name=None):
#     def inner(func):
#         nonlocal name
#         if name is None:
#             name = func.__name__

#         @Function.named_py(name)
#         def wrapper(ctx: EvalContext, exprs: List[Expr]) -> Expr:
#             func(ctx, exprs)
#             return Funcall(name, exprs)

#         return wrapper
#     return inner

ctx = bex.EvalContext(bex.Scope.from_funcions(
    # my_func,
    # my_func2,
))


bex.interpret(bex.parse_source(Path("tests/_loop_cmp.bex").read_text()))

bex.run_interactive_mode(ctx)

breakpoint
