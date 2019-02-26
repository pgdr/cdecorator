def strip(s):
    if '\n' in s:
        return '\n'.join( [ strip(l.strip()) for l in s.split('\n')  ] )
    s = s.replace(',', ', ')
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s.strip()
