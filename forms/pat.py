from math import cos, sin, atan2, hypot, pi

key_set = ('X', 'Y', 'H', 'W', 'A')
'''
def parse2 (file):
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
        
        stack.append(add(X, Y, H, W, A))
    return stack
'''
def parse (file):
    pat = list()
    elem = dict.fromkeys(key_set)
    for line in file:
        if '$' in line: break
        temp = ''
        key = None
        for char in line:
            if char == ';': break
            elif char.isalpha():
                if key:
                    elem[key] = int(temp)
                    temp = ''
                key = char
            elif char.isdigit():
                temp += char
        if key and temp != '':
            elem[key] = int(temp)
        pat.append(elem.copy())
    return pat

def build (pat, full=False):
    text = list()
    prev = dict.fromkeys(key_set)
    for item in pat:
        line = []
        for key in key_set:
            if item[key] != prev[key] or full:
                line.append(key)
                line.append(str(item[key]))
                prev[key] = item[key]
        line.append(';\n')
        text.append(''.join(line))
    text.append('$;\n')
    return ''.join(text)

def dxf (pat, layer='FROM_PAT'):
    text = [
        '  0', 'SECTION',
        '  2', 'ENTITIES'
        ]
    for item in pat:
        entry = [
            '  0', 'POLYLINE',
            '  8', layer,
            ' 66', '     1'
            ]
        if item['H'] >= item['W']:
            width = str(item['W']/1000)
            x = item['H'] * sin( item['A'] * pi / 1800 ) / 2
            y = item['H'] * cos( item['A'] * pi / 1800 ) / 2
            entry.extend((
                ' 40', width,
                ' 41', width,
                '  0', 'VERTEX',
                '  8', layer,
                ' 10', str((item['X'] + x) / 1000),
                ' 20', str((item['Y'] - y) / 1000),
                '  0', 'VERTEX',
                '  8', layer,
                ' 10', str((item['X'] - x) / 1000),
                ' 20', str((item['Y'] + y) / 1000)
                ))
        else:
            width = str(item['H']/1000)
            x = item['W'] * cos( item['A'] * pi / 1800 ) / 2
            y = item['W'] * sin( item['A'] * pi / 1800 ) / 2
            entry.extend((
                ' 40', width,
                ' 41', width,
                '  0', 'VERTEX',
                '  8', layer,
                ' 10', str((item['X'] - x) / 1000),
                ' 20', str((item['Y'] - y) / 1000),
                '  0', 'VERTEX',
                '  8', layer,
                ' 10', str((item['X'] + x) / 1000),
                ' 20', str((item['Y'] + y) / 1000)
                ))
        entry.extend((
            '  0', 'SEQEND',
            '  8', layer
            ))
        text.extend(entry)
    text.extend((
        '  0', 'ENDSEC',
        '  0', 'EOF',
        ''
        ))
    return '\n'.join(text)

def add (X=0, Y=0, H=4, W=4, A=0):
    '''while A > 1800 or A <= -1800:
        if A > 1800: A -= 3600
        if A <= -1800: A += 3600
    if A < -900:
        A += 1800
    elif -900 <= A < 0:
        A += 900
        H, W = W, H
    elif 900 >= A:
        A -= 900
        H, W = W, H'''
    elem = {
        'X': X,
        'Y': Y,
        'H': H,
        'W': W,
        'A': A
        }
    return elem

def normalize (pat):
    result = []
    for item in pat:
        A = item['A']
        H = item['H']
        W = item['W']
        while A < 0 or A >= 1800:
            if A >= 1800: A -= 1800
            if A < 0 : A += 1800
        if A >= 900:
            A -= 900
            H, W = W, H
        result.append({
            'X': round(item['X']),
            'Y': round(item['Y']),
            'H': round(H),
            'W': round(W),
            'A': round(A)
            })
    return result

def mult (elem, value=1, center=(0, 0)):
    new = add(
        X = round((elem['X']-center[0]) * value) + center[0],
        Y = round((elem['Y']-center[1]) * value) + center[1],
        H = round(elem['H'] * value),
        W = round(elem['W'] * value),
        A = elem['A']
        )
    return new

def mult_all (pat, value=1, center=(0, 0)):
    result = []
    for elem in pat:
        result.append(
            mult(elem, value, center))
    return result

def rotate (elem, ang=0, cent=(51000, 51000)):
    while ang > 1800 or ang <= -1800:
        if ang > 1800: ang = ang - 3600
        if ang <= -1800: ang = ang + 3600
    turned = turn(elem, ang)
    new = add(
        X = round(cos(atan2(elem['Y']-cent[1],
                          elem['X']-cent[0])
                    + (ang * pi / 1800) )
                * hypot(elem['Y']-cent[1],
                        elem['X']-cent[0]) ) + cent[0],
        Y = round(sin(atan2(elem['Y']-cent[1],
                          elem['X']-cent[0])
                    + (ang * pi / 1800) )
                * hypot(elem['Y']-cent[1],
                        elem['X']-cent[0]) ) + cent[1],
        H = turned['H'],
        W = turned['W'],
        A = turned['A']
        )    
    return new

def rot_all (pat, ang=0, cent=(51000, 51000)):
    result = []
    for elem in pat:
        result.append(
            rotate(elem, ang, cent))
    return result

def move (elem, end=(0, 0), start=(0, 0)):
    if start != (0, 0):
        dist = (end[0]-start[0], end[1]-start[1])
    else: dist = end
    new = add(
        X = elem['X'] + dist[0],
        Y = elem['Y'] + dist[1],
        H = elem['H'],
        W = elem['W'],
        A = elem['A']
        )
    return new

def move_all (pat, end=(0, 0), start=(0, 0)):
    result = []
    for elem in pat:
        result.append(
            move(elem, end, start))
    return result

def turn (elem, ang=0):
    while ang > 1800 or ang <= -1800:
        if ang > 1800: ang = ang - 3600
        if ang <= -1800: ang = ang + 3600
    new = dict.fromkeys(key_set)
    for key in ('X', 'Y'):
        new[key] = elem[key]
    new_ang = elem['A'] + ang
    if new_ang >= 1800:
        new['H'] = elem['H']
        new['W'] = elem['W']
        new['A'] = new_ang - 1800
    elif 1800 > new_ang >= 900:
        new['H'] = elem['W']
        new['W'] = elem['H']
        new['A'] = new_ang - 900
    elif 900 > new_ang >= 0:
        new['H'] = elem['H']
        new['W'] = elem['W']
        new['A'] = new_ang
    elif 0 > new_ang >= -900:
        new['H'] = elem['W']
        new['W'] = elem['H']
        new['A'] = new_ang + 900
    else:
        new['H'] = elem['H']
        new['W'] = elem['W']
        new['A'] = new_ang + 1800
    return new

def turn_all (pat, ang=0):
    result = []
    for elem in pat:
        result.append(
            turn(elem, ang))
    return result

def extend (elem, enlarge=(0, 0)):
    new = add(
        X = elem['X'],
        Y = elem['Y'],
        H = elem['H'] + enlarge[0],
        W = elem['W'] + enlarge[1],
        A = elem['A']
        )
    return new

def ext_all (pat, enlarge=(0, 0)):
    result = []
    for elem in pat:
        result.append(
            extend(elem, enlarge))
    return result

def sort (pat, key='A'):
    stack = dict()
    key_max = 0
    for item in pat:
        if not item[key] in stack:
            stack[item[key]] = [item]
        else:
            stack[item[key]].append(item)
        if item[key] > key_max: key_max = item[key]
    result = []
    for i in range(key_max+1):
        if i in stack:
            for item in stack[i]:
                result.append(item)
    return result
