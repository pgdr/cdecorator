def strip(s):
    if '\n' in s:
        return '\n'.join( [ strip(l.strip()) for l in s.split('\n')  ] )
    while '  ' in s:
        s.replace('  ', ' ')
    return s.strip()
