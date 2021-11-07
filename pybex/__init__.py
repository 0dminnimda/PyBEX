__version__ = "0.0.2"
__name__ = "pybex"

from .builtins import builtin_scope
from .classes import EvalContext, Scope
from .run import interpret, run_interactive_mode
from .parser import parse_source
