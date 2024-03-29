from ..classes import Scope
from .classtype import classtype
from .collections import collections
from .conditions import conditions
from .core import core
from .function import function
from .inout import inout
from .loop import loop
from .number import number
from .string import string
from .timemodule import timemodule

builtin_scope = Scope.from_funcions(
    *classtype,
    *collections,
    *conditions,
    *core,
    *function,
    *inout,
    *loop,
    *number,
    *string,
    *timemodule,
)
