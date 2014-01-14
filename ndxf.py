def ndxf (dxf):
    new = ''
    while param == '  0\n' and value == 'EOF\n':
        while (
            param != '  2\n' and
            value != 'ENTITIES\n'
            ):
            param = dxf.readline()
            value = dxf.readline()
        else :
            new += '  0\n'+'SECTION\n' + param + value
        while (
            param = '  0\n' and (
                value = 'POLYLINE\n' or
                value = 'VERTEX\n' or
                value = 'SOLID\n' or
                value = 'SEQEND\n'
