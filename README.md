# **Py**thon **B**ot **EX**pression (PyBEX)

A simple Interpreted Dynamic Programming Language for describing chat bot commands and behavior.

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
f("can take in any other element")
```

## Interactive mode

```
bex> say(99,
 ... "bottles of beer",
 ... "on the wall.")
99 bottles of beer on the wall.
bex> if(1, "pi", 3.1415)
'pi'
```

[Inspiration for the project](https://gitlab.com/tsoding/bex)
