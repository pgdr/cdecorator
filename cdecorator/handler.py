import typing
import ast

_HANDLE = {
}

def handle(expr):
    return _HANDLE[ type(expr) ] (expr)

def _strip(s):
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s.strip()

def ast_num(expr):
    return f'{expr.n}'

def ast_constant(expr):  # new in Python 3.6
    return f'{expr.n}'

def ast_index(expr):
    return expr.value.id

def ast_name(expr):
    return f'{expr.id}'

def ast_call(expr):
    args = ', '.join( [ handle(arg) for arg in expr.args ] )
    return _strip(f'{expr.func.id}({args})')

def ast_subscript(expr):
    return _strip(f'{handle(expr.value)} {handle(expr.slice)}')

def ast_return(expr):
    return f'return {handle(expr.value)};'

def ast_annassign(expr):
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

def ast_assign(expr):
    return f'{handle(expr.targets[0])} = {handle(expr.value)};'

def ast_functiondef(expr):
    fname = expr.name
    ass_ = []
    for x in expr.body:
        ass_.append(handle(x))
    body = '\n    '.join(ass_)
    return f'void {fname}() ' + '{\n' + body + '\n}'

_HANDLE[ast.AnnAssign]   = ast_annassign
_HANDLE[ast.Assign]      = ast_assign
_HANDLE[ast.FunctionDef] = ast_functiondef
_HANDLE[ast.Return]      = ast_return
_HANDLE[ast.Call]        = ast_call
_HANDLE[ast.Subscript]   = ast_subscript
_HANDLE[ast.Name]        = ast_name
_HANDLE[ast.Num]         = ast_num
_HANDLE[ast.Constant]    = ast_constant
_HANDLE[ast.Index]       = ast_index
