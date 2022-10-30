from ..classes import Scope
from .classtype import classtype
from .collections import collections
from .conditions import conditions
from .core import core
from .function import function
from .inout import inout
from .number import number
from .string import string

builtin_scope = Scope.from_funcions(
    *classtype,
    *collections,
    *conditions,
    *core,
    *function,
    *inout,
    *number,
    *string,
)
