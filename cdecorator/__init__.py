import typing
import ast
import inspect

_HANDLE = {
}

def handle(expr):
    return _HANDLE[ type(expr) ] (expr)

def _strip(s):
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s.strip()

def num(expr):
    return f'{expr.n}'

def index(expr):
    return expr.value.id

def name(expr):
    return f'{expr.id}'

def call(expr):
    args = ', '.join( [ handle(arg) for arg in expr.args ] )
    return _strip(f'{expr.func.id}({args})')

def subscript(expr):
    return _strip(f'{handle(expr.value)} {handle(expr.slice)}')

def return_(expr):
    return f'return {handle(expr.value)};'

def annassign(expr):
    target = expr.target.id
    ann = handle(expr.annotation)
    value = ''
    try:
        value = expr.value
    except Exception as e:
        print(e)

    if value:
        value = handle(value)
    try:
        slice_ = expr.annotation.slice.value.id
    except:
        slice_ = ''
    if value:
        return _strip('{} {} {} = {};'.format(ann, target, slice_, value))
    return _strip('{} {};'.format(ann, target))

def assign(expr):
    return f'{handle(expr.targets[0])} = {handle(expr.value)};'

def functiondef(expr):
    fname = expr.name
    ass_ = []
    for x in expr.body:
        ass_.append(handle(x))
    body = '\n    '.join(ass_)
    return f'void {fname}() ' + '{\n' + body + '\n}'

_HANDLE[ast.AnnAssign]   = annassign
_HANDLE[ast.Assign]      = assign
_HANDLE[ast.FunctionDef] = functiondef
_HANDLE[ast.Return]      = return_
_HANDLE[ast.Call]        = call
_HANDLE[ast.Subscript]   = subscript
_HANDLE[ast.Name]        = name
_HANDLE[ast.Num]         = num
_HANDLE[ast.Index]       = index


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
