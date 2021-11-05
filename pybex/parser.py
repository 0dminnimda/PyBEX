import os
from lark import Lark, Transformer
import ast

from .classes import Funcall, Number, Program, String, Word


class BEXTransformer(Transformer):
    def int(self, items):
        return Number(int(items[0].value))

    def float(self, items):
        return Number(float(items[0].value))

    def string(self, items):
        return String(ast.literal_eval(items[0].value))

    def word(self, items):
        return Word(items[0].value)

    def funcall(self, items):
        return Funcall(items[0].value, items[1:])

    def start(self, items):
        return Program(items)


with open(os.path.join(os.path.dirname(__file__), "grammar.lark")) as f:
    PARSER = Lark(f)
    del f


def parse_source(source: str) -> Program:
    return BEXTransformer().transform(PARSER.parse(source))


def parse_file(path: str) -> Program:
    with open(path) as f:
        return parse_source(f.read())
