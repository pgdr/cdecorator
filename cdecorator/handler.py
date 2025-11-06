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


def _transformer(expr):
    args = ', '.join( [ handle(arg) for arg in expr.args ] )
    return _strip(f'<{args}>')


def _include(expr):
    args = ', '.join( [ handle(arg) for arg in expr.args ] )
    if args.startswith('"<'):
        args = args[1:-1]
        return _strip(f'#include {args}')
    return _strip(f'#include {args}')


def ast_num(expr):
    return f'{expr.n}'


def ast_str(expr):
    return f'"{expr.value}"'



def ast_constant(expr):
    match expr.value:
        case str():
            return ast_str(expr)
        case int():
            return ast_num(expr)
        case float():
            return ast_float(expr)
        case bool():
            return ast_bool(expr)
        case _:
            raise ValueError(f"Unsupported type: {type(expr.value)} for {expr.value}")


def ast_index(expr):
    return expr.value.id


def ast_name(expr):
    return f'{expr.id}'


def ast_call(expr):
    func = handle(expr.func)
    if func == '_':  # this is the <transformer> syntax
        return _transformer(expr)
    if func == '__include__':
        return _include(expr)
    if func == 'print':
        func = 'printf'  # close enough
    args = ', '.join( [ handle(arg) for arg in expr.args ] )
    return _strip(f'{func}({args})')

def ast_subscript(expr):
    slic = handle(expr.slice)
    val = handle(expr.value)
    return _strip(f'{val} {slic}')

def ast_return(expr):
    return f'return {handle(expr.value)};'

def ast_annassign(expr):
    target = handle(expr.target)
    ann = handle(expr.annotation)
    value = handle(expr.value) if expr.value is not None else ''

    try:
        slice_ = expr.annotation.slice.value.id
    except:
        slice_ = ''
    if value:
        return _strip('{} {} = {};'.format(ann, target, value))
    return _strip('{} {};'.format(ann, target))


def ast_compare(expr):
    left = handle(expr.left)
    comps = [handle(comp) for comp in expr.comparators]
    ops = [handle(op) for op in expr.ops]
    return f'{left} {ops[0]} {comps[0]}'


def ast_if(expr):
    test = handle(expr.test)
    body = [handle(line) for line in expr.body]
    orelse = expr.orelse
    return f'if ({test}) ' + '{\n' + '\n'.join(body) + '\n}'


def ast_unaryop(expr):
    operand = handle(expr.operand)
    op = handle(expr.op)
    return f'{op} {operand}'


def ast_binop(expr):
    left  = handle(expr.left)
    right = handle(expr.right)
    op = handle(expr.op)
    return f'{left} {op} {right}'


def ast_matmult(expr):
    return '@'


def ast_attribute(expr):
    val = handle(expr.value)
    attr = expr.attr  # str
    return f'{val}.{attr}'


def ast_expr(expr):
    val = handle(expr.value)
    if val.startswith("#include"):
        return f'{val}'
    return f'{val};'


def ast_assign(expr):
    t0 = handle(expr.targets[0])
    val = handle(expr.value)
    return f'{t0} = {val};'


def ast_augassign(expr):
    target = handle(expr.target)
    op = handle(expr.op)
    val = handle(expr.value)
    return f'{target} {op} {val};'


def ast_arg(expr):
    arg = handle(expr.arg)
    if expr.annotation:
        ann = handle(expr.annotation)
        return f'{ann} {arg}'  # the space is annoying
    return f'{arg}'


def ast_arguments(expr):
    return ','.join(
        [handle(arg) for arg in expr.args]
    )


def ast_functiondef(expr):
    returns = handle(expr.returns) if expr.returns else 'void'
    fname = expr.name if type(expr.name) == str else handle(expr.name)
    args = handle(expr.args)
    ass_ = []
    for x in expr.body:
        ass_.append(handle(x))
    body = '\n    '.join(ass_)
    return f'{returns} {fname}({args}) ' + '{\n' + body + '\n}'


def constant(elt):
    return lambda _ : elt

def identity(elt):
    return elt

_HANDLE[ast.AnnAssign]   = ast_annassign
_HANDLE[ast.Assign]      = ast_assign
_HANDLE[ast.AugAssign]   = ast_augassign
_HANDLE[ast.FunctionDef] = ast_functiondef
_HANDLE[ast.Return]      = ast_return
_HANDLE[ast.Call]        = ast_call
_HANDLE[ast.Compare]     = ast_compare
_HANDLE[ast.Subscript]   = ast_subscript
_HANDLE[ast.Name]        = ast_name
_HANDLE[ast.Num]         = ast_num
_HANDLE[ast.Str]         = ast_str
_HANDLE[str]             = identity
_HANDLE[ast.Constant]    = ast_constant
_HANDLE[ast.Index]       = ast_index
_HANDLE[ast.arguments]   = ast_arguments
_HANDLE[ast.arg]         = ast_arg
_HANDLE[ast.If]          = ast_if
_HANDLE[ast.UnaryOp]     = ast_unaryop
_HANDLE[ast.BinOp]       = ast_binop
_HANDLE[ast.Attribute]   = ast_attribute
_HANDLE[ast.Expr]        = ast_expr
_HANDLE[ast.Lt]          = constant('<')
_HANDLE[ast.LtE]         = constant('<=')
_HANDLE[ast.Gt]          = constant('>')
_HANDLE[ast.Mult]        = constant('*')
_HANDLE[ast.Div]         = constant('/')
_HANDLE[ast.Add]         = constant('+')
_HANDLE[ast.Sub]         = constant('-')
_HANDLE[ast.USub]        = constant('-')
_HANDLE[ast.MatMult]     = ast_matmult
