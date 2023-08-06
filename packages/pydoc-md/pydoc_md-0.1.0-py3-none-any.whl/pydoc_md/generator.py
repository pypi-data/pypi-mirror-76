from .parser import Module, Routine


def gen(mod: Module) -> str:
    ret = ""
    for fn in mod.functions.values():
        ret += gen_func(fn)
    return ret


def gen_code(code: str) -> str:
    return f"""```python
{code}
```

"""


def gen_func(fn: Routine) -> str:
    name = fn.name
    ret = f"### `{name}`\n\n"
    if fn.signature:
        ret += gen_code(f"def {name}{str(fn.signature)}: ...")
    if fn.short_description:
        ret += fn.short_description + "\n\n"
    if fn.long_description:
        ret += fn.long_description + "\n\n"
    if fn.example_code:
        ret += gen_code(fn.example_code)
    return ret

