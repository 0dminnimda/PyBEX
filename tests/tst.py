from pybex import run_interactive_mode


# print(result)

program_body = '''
say("""long
word""",
"and multiline func")
say("Hello", "world!")
say("I am", name, "!")

"""dfgdfg5675"""

56456
45645.4546
1_000_000

say(if(1, 6, 8))  # 6
say(this(say()))  # Funcall(name='say', args=[])

say(this(say(pi, 31415, this(), if)))
# Funcall(name='say', args=[
#     Word(value='pi'), 31415,
#     Funcall(name='this', args=[]), Word(value='if')])

'''

# interpret(ctx, parse_source(program_body))

run_interactive_mode()


breakpoint
