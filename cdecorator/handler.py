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
    if expr.n == Ellipsis:
        return '<'
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

def ast_compare(expr):
    left = handle(expr.left)
    comps = [handle(comp) for comp in expr.comparators]
    ops = [handle(op) for op in expr.ops]
    return f'{left} OP {comps[0]}'

def ast_binop(expr):
    left  = handle(expr.left)
    right = handle(expr.right)
    op = handle(expr.op)
    if op == '@':   # this is hijacked for <operator>
        return f'<{right}>'
    return f'{left} {op} {right}'


def ast_matmult(expr):
    return '@'


def ast_attribute(expr):
    val = handle(expr.value)
    attr = expr.attr  # str
    return f'{val}.{attr}'


def ast_assign(expr):
    t0 = handle(expr.targets[0])
    val = handle(expr.value)
    return f'{t0} = {val};'


def ast_arg(expr):
    arg = handle(expr.arg)
    return f'{arg}'


def ast_arguments(expr):
    return ','.join(
        [handle(arg) for arg in expr.args]
    )


def ast_functiondef(expr):
    fname = expr.name
    args = expr.args.args
    if args:
        args = [arg.arg for arg in args]
    ass_ = []
    for x in expr.body:
        ass_.append(handle(x))
    body = '\n    '.join(ass_)
    return f'void {fname}({", ".join(args)}) ' + '{\n' + body + '\n}'


_HANDLE[ast.AnnAssign]   = ast_annassign
_HANDLE[ast.Assign]      = ast_assign
_HANDLE[ast.FunctionDef] = ast_functiondef
_HANDLE[ast.Return]      = ast_return
_HANDLE[ast.Call]        = ast_call
_HANDLE[ast.Compare]     = ast_compare
_HANDLE[ast.Subscript]   = ast_subscript
_HANDLE[ast.Name]        = ast_name
_HANDLE[ast.Num]         = ast_num
_HANDLE[ast.Constant]    = ast_constant
_HANDLE[ast.Index]       = ast_index
_HANDLE[ast.arguments]   = ast_arguments
_HANDLE[ast.arg]         = ast_arg
_HANDLE[ast.BinOp]       = ast_binop
_HANDLE[ast.Attribute]   = ast_attribute
_HANDLE[ast.Lt]          = lambda _ : '<'
_HANDLE[ast.Gt]          = lambda _ : '>'
_HANDLE[ast.Mult]        = lambda _ : '*'
_HANDLE[ast.Div]         = lambda _ : '/'
_HANDLE[ast.Add]         = lambda _ : '+'
_HANDLE[ast.MatMult]     = ast_matmult
