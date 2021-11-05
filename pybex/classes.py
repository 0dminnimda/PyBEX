from typing import Callable, Dict, List, Union
from dataclasses import dataclass


class Expr:
    pass


@dataclass
class Program:
    body: List[Expr]


class Nothing(Expr):
    pass


@dataclass
class Number(Expr):
    value: Union[int, float]


@dataclass
class String(Expr):
    value: str


@dataclass
class Word(Expr):
    value: str


@dataclass
class Funcall(Expr):
    func_name: str
    body: List[Expr]


@dataclass
class EvalContext:
    namespase: Dict[str, Union["Function", object]]


class Function:
    def __init__(self, func: Callable[[EvalContext, List[Expr]], Expr]):
        self.func = func

    def __call__(self, ctx: EvalContext, exprs: List[Expr]) -> Expr:
        return self.func(ctx, exprs)
