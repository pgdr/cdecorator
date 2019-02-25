import ast
import inspect

from .handler import handle


def transpile(func):
    tree = ast.parse(inspect.getsource(func))
    fdef = tree.body[0]
    body = fdef.body
    name = fdef.name

    exprs = []

    for expr in body:
        res = handle(expr)
        exprs.append(res)

    return '\n'.join(exprs).strip()

def transpiler(name):
    def wrapper(f):
        def inner():
            return transpile(f)
        return inner
    return wrapper
