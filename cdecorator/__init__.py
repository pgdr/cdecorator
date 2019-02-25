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

class _callable_str:
    def __init__(self, s):
        self.s = s
    def __call__(self, *args, **kwargs):
        return self.s
    def __str__(self):
        return self.s
    def __repr__(self):
        return self.s

def transpiler(f):
    return transpile(f)
