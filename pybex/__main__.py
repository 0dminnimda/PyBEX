import argparse

from pybex import EvalContext, interpret, parse_source, run_interactive_mode

parser = argparse.ArgumentParser(
    prog="pybex", description="Run PyBEX programming language interpreter")

parser.add_argument("file", nargs="?", help="path of the script file")

args = parser.parse_args()

if args.file is None:
    run_interactive_mode()
else:
    with open(args.file, encoding="utf-8") as f:
        source = f.read()
    interpret(parse_source(source))
