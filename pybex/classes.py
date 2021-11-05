from typing import Callable, Dict, List, Type, Union, TypeVar
from dataclasses import dataclass
from functools import partial


# Interpretation

@dataclass
class EvalContext:
    namespase: Dict[str, Union["Function", object]]


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
        return f"Function<{self._func.__name__}>"


# AST/code Constants


class NothingType(Expr):
    def __repr__(self):
        return "Nothing"


Nothing = NothingType()


class UnfinishedType(Expr):
    pass


Unfinished = UnfinishedType()
