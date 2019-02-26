import ast
import inspect

from .handler import handle


def compile(func):
    import os
    import tempfile
    fname = tempfile.NamedTemporaryFile(delete=False, suffix='.c')
    out   = tempfile.NamedTemporaryFile(delete=False, suffix='.out')
    source = transpile(func)
    with open(fname.name, 'w') as f:
        f.write(source)
    cmd = ' '.join(['gcc', '-fPIC',  '--shared', fname.name, '-o', out.name])
    os.system(cmd)
    import ctypes
    return ctypes.cdll.LoadLibrary(out.name)


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
