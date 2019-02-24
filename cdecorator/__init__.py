import typing
import ast
import inspect

_HANDLE = {
}

def num(expr):
    return f'{expr.n}'

def return_(expr):
    return f'return {_HANDLE[type(expr.value)](expr.value)};'

def annassign(expr):
    var = f'{expr.annotation.value.id.lower()} {expr.annotation.slice.value.id} {expr.target.id};'
    return var

def assign(expr):
    return f'{expr.value.id} = {expr.targets[0].id};'

def functiondef(expr):
    fname = expr.name
    ass_ = []
    for x in expr.body:
        ass_.append(_HANDLE[type(x)](x))
    body = '\n    '.join(ass_)
    return f'void {fname}() ' + '{\n' + body + '\n}'

_HANDLE[ast.AnnAssign]   = annassign
_HANDLE[ast.Assign]      = assign
_HANDLE[ast.FunctionDef] = functiondef
_HANDLE[ast.Return]      = return_
_HANDLE[ast.Num]         = num


def transpile(func):
    tree = ast.parse(inspect.getsource(func))
    fdef = tree.body[0]
    body = fdef.body
    name = fdef.name

    exprs = []

    for expr in body:
        res = _HANDLE[type(expr)](expr)
        exprs.append(res)

    return '\n'.join(exprs).strip()

def transpiler(name):
    def wrapper(f):
        def inner():
            return transpile(f)
        return inner
    return wrapper
