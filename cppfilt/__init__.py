MSVC_PARAMS = {
}

def demangle_msvc(src):
    namespace = []
    params    = []
    namestr = ''
    paramflag = False

    for c in src:
        if not paramflag:
            if len(namestr) > 0 and c == '@':
                namespace.append(namestr)
                namestr = ''
                continue
            if c == '@':
                paramflag = True
                continue
            namestr += c
        else:
            if c == '@':
                break
            # params.append(MSVC_PARAMS[c])

    namespace.reverse()
    return '::'.join(namespace) + '()'

GCC_PARAMS = {
    'i': 'int',
    'f': 'float',
}

def demangle_gcc(src):
    namespace = []
    params    = []
    cnt = 0
    cntstr = ''
    namestr = ''
    if src.startswith('N'):
        namespaceflag = True
        src = src[1:]
    else:
        namespaceflag = False

    for c in src:
        if len(cntstr) > 0 and not c.isdigit():
            cnt = int(cntstr)
            cntstr = ''

        if len(namestr) > 0 and cnt == 0:
            namespace.append(namestr)
            namestr = ''

        if cnt > 0:
            namestr += c
            cnt -= 1
            continue

        if c.isdigit():
            cntstr += c
            continue

        if namespaceflag and c == 'E':
            namespaceflag = False
            continue

        if not namespaceflag:
            params.append(GCC_PARAMS[c])

    return '::'.join(namespace) + '(%s)' % ','.join(params)

def demangle(src):
    if src.startswith('_Z'):
        return demangle_gcc(src[2:])
    if src.startswith('?'):
        return demangle_msvc(src[1:])
    return ''
    