def read (file):
    stack = []
    X = Y = H = W = A = 0
    for line in file:
        if '$' in line: break
        
        X1 = line.find('X')
        Y1 = line.find('Y')
        H1 = line.find('H')
        W1 = line.find('W')
        A1 = line.find('A')
        A2 = line.find(';')
        
        if   Y1 > -1: X2 = Y1
        elif H1 > -1: X2 = H1
        elif W1 > -1: X2 = W1
        elif A1 > -1: X2 = A1
        else: X2 = A2
        
        if   H1 > -1: Y2 = H1
        elif W1 > -1: Y2 = W1
        elif A1 > -1: Y2 = A1
        else: Y2 = A2
        
        if   W1 > -1: H2 = W1
        elif A1 > -1: H2 = A1
        else: H2 = A2
        
        if   A1 > -1: W2 = A1
        else: W2 = A2
        
        if X1 > -1: X = int(line[X1+1:X2])
        if Y1 > -1: Y = int(line[Y1+1:Y2])
        if H1 > -1: H = int(line[H1+1:H2])
        if W1 > -1: W = int(line[W1+1:W2])
        if A1 > -1: A = int(line[A1+1:A2])
        
        stack.append({
            'X': X,
            'Y': Y,
            'H': H,
            'W': W,
            'A': A
            })
    return stack

def build (stack, full=False):
    text = []
    X = Y = H = W = A = 0
    prev = {
        'X': None,
        'Y': None,
        'H': None,
        'W': None,
        'A': None
        }
    for item in stack:
        line = []
        for key in item:
            if item[key] != prev[key] or full:
                line.append(key)
                line.append(str(item[key]))
                prev[key] = item[key]
        line.append(';\n')
        text.append(''.join(line))
    text.append('$;\n')
    return ''.join(text)
