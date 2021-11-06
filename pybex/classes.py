from dataclasses import dataclass, field
from functools import partial
from typing import Callable, Dict, List, Optional, Type, TypeVar, Union


# Interpretation

@dataclass
class Scope:
    namespace: Dict[str, "Expr"] = field(
        default_factory=dict)

    def update_by_scope(self, scope: "Scope") -> None:
        self.namespace.update(scope.namespace)


class EvalContext:
    scopes: List[Scope]
    last_funcall: Optional["Funcall"]

    def __init__(self, scope: Optional[Scope] = None):
        if scope is None:
            scope = Scope()
        self.scopes = [scope]
        self.last_funcall = None

    @property
    def scope(self) -> Scope:
        return self.scopes[-1]

    def add_scope(self, scope: Scope) -> None:
        self.scopes.append(scope)

    def add_new_scope(self) -> None:
        self.add_scope(Scope())

    def pop_scope(self) -> None:
        if len(self.scopes) == 0:
            raise RuntimeError("Cannot removethe only one last scope, "
                               "there always should be at least one left")

        del self.scopes[-1]


# AST

class Expr:
    pass


@dataclass
class Program:
    body: List[Expr]


@dataclass
class Number(Expr):
    value: Union[int, float]

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return str(self.value)


@dataclass
class String(Expr):
    value: str

    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        return self.value


@dataclass
class Word(Expr):
    value: str


@dataclass
class Funcall(Expr):
    name: str
    args: List[Expr]


PyFunctionT = Callable[[EvalContext, List[Expr]], Expr]
FuncT = TypeVar("FuncT", bound="Function")


@dataclass
class Function(Expr):
    name: str
    _func: PyFunctionT

    @classmethod
    def named_py(cls: Type[FuncT],
                 name: str) -> Callable[[PyFunctionT], FuncT]:
        return partial(cls, name)

    @classmethod
    def py(cls: Type[FuncT], func: PyFunctionT) -> FuncT:
        return cls(func.__name__, func)

    # too dynamic for type checkers:
    # @classmethod
    # def py(
    #     cls: Type[FuncT], arg1: Union[PyFunctionT, str]
    # ) -> Union[FuncT, Callable[[PyFunctionT], FuncT]]:

    #     if isinstance(arg1, str):
    #         return partial(cls, arg1)
    #     return cls(arg1.__name__, arg1)

    def __call__(self, ctx: EvalContext, exprs: List[Expr]) -> Expr:
        return self._func(ctx, exprs)

    def __repr__(self):
        return f"Function(name={self.name!r})"


# AST/code Constants


class NothingType(Expr):
    def __repr__(self):
        return "Nothing"


Nothing = NothingType()


class UnfinishedType(Expr):
    pass


Unfinished = UnfinishedType()
