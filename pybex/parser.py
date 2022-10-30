import ast
from dataclasses import dataclass

from lark import Lark, Transformer

from .classes import Funcall, Number, Program, String, Unfinished, Word


@dataclass
class BEXTransformer(Transformer):
    interactive: bool

    def int(self, items):
        return Number(int(items[0].value))

    def float(self, items):
        return Number(float(items[0].value))

    def string(self, items):
        return String(ast.literal_eval(items[0].value))

    def unfinished_string(self, items):
        if self.interactive:
            return Unfinished
        # TODO: pretty parsing errors
        raise SyntaxError("unterminated triple-quoted string literal")

    def word(self, items):
        return Word(items[0].value)

    def funcall(self, items):
        return Funcall(items[0].value, items[1:])

    def unfinished_call(self, items):
        if self.interactive:
            return Unfinished
        # TODO: pretty parsing errors
        raise SyntaxError("unexpected EOF while parsing")

    def exec_input(self, items):
        return Program(items)

    def single_input(self, items):
        return Program(items)


_transformer = BEXTransformer(False)
_parser = Lark.open(
    "grammar.lark", parser="lalr", transformer=_transformer,
    start=["single_input", "exec_input"], rel_to=__file__,
    maybe_placeholders=False,
    # priority="invert"
    # debug=True,
    # propagate_positions=True,
)


def parse_source(source: str, mode: str = "exec") -> Program:
    if mode == "exec":
        _transformer.interactive = False
        start = "exec_input"
    # elif mode == "eval":
    #     _transformer.interactive = False
    #     start = "expr"
    elif mode == "single":
        _transformer.interactive = True
        start = "single_input"
    else:
        raise ValueError("`mode` must be 'exec'"
                         # ", 'eval'"
                         " or 'single'")

    # _parser.parse_interactive
    return _parser.parse(source, start=start)  # type: ignore


# def parse_file(path: str, mode: str = "exec") -> Program:
#     with open(path) as f:
#         return parse_source(f.read(), mode)
