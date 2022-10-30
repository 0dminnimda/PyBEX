__version__ = "0.0.2"
__name__ = "pybex"

from .builtins import builtin_scope
from .classes import (
    EvalContext,
    Expr,
    Funcall,
    Function,
    Nothing,
    Number,
    Scope,
    String,
    Word,
)
from .interpreter import (
    assert_arg_type,
    assert_args_amount,
    eval_expr,
    eval_funcall,
    eval_word,
    raise_argument_error,
)
from .parser import parse_source
from .run import interpret, run_interactive_mode
