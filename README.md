# **Py**thon **B**ot **EX**pression (PyBEX)

A simple Interpreted Dynamic Programming Language for describing chat bot commands and behavior.

## Installing PyBEX

PyBEX is available on PyPI:

```console
python -m pip install -U pybex
```

## Language Elements

### String

```
"Hello, World"

'single or double - doesn\'t matter'

"""multiline
ones"""

'''are
supported'''
```

### Number

```
# integers
69
420
1_000_000  # 1000000

# and floats
3.1415
5e-10
```

### Variable

```
args
sender
_underscore
```

### Funcalls

```
f()
f(g())
f(69, 420, 3.1415)
f("can take in any other language element")
```

## Interactive mode

use command:
```console
python -m pybex
```

```
bex> say(99,
 ... "bottles of beer",
 ... "on the wall.")
99 bottles of beer on the wall.
bex> if(1, "pi", 3.1415)
'pi'
```

## Interpret from the file

use command:
```console
python -m pybex <file_path>
```

(replace <file_path> with path of your script file)

```
say(if(
    int(input()),
    "non-zero input",
    "zero input"
))
```

## Examples

You can see more code examples in [`tests`](/tests) folder

### How to add my own functions?

Don't be scared, it's quite easy!

Here you can see how to create two functions `this_is` and `ninja`:

Run this code and see the output for yourself!

```python
from typing import List
import random

import pybex as bex


bad_code = True


@bex.Function.py  # bex_this_is.name == "this_is"
def bex_this_is(ctx: bex.EvalContext, exprs: List[bex.Expr]) -> bex.Expr:
    bex.assert_args_amount(ctx, exprs, "==", 0)

    global bad_code
    if bad_code:
        print("sparta")
    else:
        print("no, this is patrick")
    bad_code = not bad_code

    return bex.Nothing


BYTES = [108, 105, 103, 109, 97]


@bex.Function.named_py("ninja")  # hidden_name.name == "ninja"
def hidden_name(ctx: bex.EvalContext, exprs: List[bex.Expr]) -> bex.Expr:
    bex.assert_args_amount(ctx, exprs, "==", 1)
    arg = bex.assert_arg_type(ctx, exprs[0], 0, bex.String)

    if arg.value == "has died of":
        return bex.String(bytes(BYTES).decode())

    as_list = list(arg.value)
    random.shuffle(as_list)
    return bex.String("".join(as_list))


ctx = bex.EvalContext(bex.Scope.from_funcions(
    bex_this_is,
    hidden_name,
))


code = """
this_is()
this_is()
this_is()
this_is()
this_is()
this_is()

say(ninja("12345"))
say(ninja("superman"))
say(ninja("has died of"))
"""

# interpret the source code
bex.interpret(bex.parse_source(code), ctx)

# or run an interactive console app
# bex.run_interactive_mode(ctx)
```

---

[Inspiration for the project](https://gitlab.com/tsoding/bex)
