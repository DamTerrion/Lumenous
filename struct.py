from dxf import load

def structurize (data, i=0, break_condition=(0, 'EOF')):
    stack = list()
    while i < len(data):
        if (data[i] == break_condition or
            (data[i][0], 'ANY') == break_condition):
            return stack
        if data[i] == (66, '1'):
            break_condition = (0, 'SEQEND')
        if data[i][0] == 0:
            if data[i][1] == 'SECTION':
                break_condition = (0, 'ENDSEC')
            elif data[i][1] == 'TABLE':
                break_condition = (0, 'ENDTAB')
            else: break_condition = (0, 'ANY')
            result = structurize(data, i, (0, 'ANY'))
        stack.append(result)
        i += 1
    return stack

A = load('E.dxf')
B = structurize(A)
