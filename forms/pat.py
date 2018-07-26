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
    elem = {
        'X': X,
        'Y': Y,
        'H': H,
        'W': W,
        'A': A
        }
    return elem

def mult (pat, value=1, center=(0, 0), copy=False):
    result = []
    if copy: result.extend(pat)
    for item in pat:
        new = dict.fromkeys(key_set)
        new['X'] = int((item['X']-center[0]) * value) + center[0]
        new['Y'] = int((item['Y']-center[1]) * value) + center[1]
        new['H'] = int(item['H'] * value)
        new['W'] = int(item['W'] * value)
        new['A'] = item['A']
        result.append(new)
    return result

def rotate (pat, ang=0, cent=(51000, 51000), copy=False):
    result = []
    if copy: result.extend(pat)
    while ang > 1800 or ang <= -1800:
        if ang > 1800: ang = ang - 3600
        if ang <= -1800: ang = ang + 3600
    for item in pat:
        new = dict.fromkeys(key_set)
        new['X'] = int(cos(
            atan2(item['Y']-cent[1], item['X']-cent[0])
            + (ang * pi / 1800)
            ) * hypot(item['Y']-cent[1], item['X']-cent[0])) + cent[0]
        new['Y'] = int(sin(
            atan2(item['Y']-cent[1], item['X']-cent[0])
            + (ang * pi / 1800)
            ) * hypot(item['Y']-cent[1], item['X']-cent[0])) + cent[1]
        turned = turn(item, ang)
        for key in ('H', 'W', 'A'):
            new[key] = turned[key]
        result.append(new)
    return result

def move (pat, end=(0, 0), start=(0, 0), copy=False):
    result = []
    if copy: result.extend(pat)
    if start != (0, 0):
        dist = (end[0]-start[0], end[1]-start[1])
    else: dist = end
    for item in pat:
        new = dict.fromkeys(key_set)
        new['X'] = item['X'] + dist[0]
        new['Y'] = item['Y'] + dist[1]
        for key in ('H', 'W', 'A'):
            new[key] = item[key]
        result.append(new)
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
