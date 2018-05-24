def parse (line):
    line = line.replace(',', '.')
    coords, last = list(), str()
    for char in line:
        if not char.isalnum() and not char == '.':
            if last:
                try:
                    new = float(last)
                except ValueError:
                    new = str(last)
                finally:
                    coords.append(new)
                    last = ''
        else:
            last += char
    return coords

def build_line (data):
    def new_poly ():
        there = layer
        return {'layer': there,
                'vertex': list()}
    
    layer = '0'
    stack, polyline = list(), new_poly()
    for line in data:
        entry = parse(line)
        if len(entry) == 0:
            if polyline['vertex']:
                stack.append(polyline)
                polyline = new_poly()
        elif len(entry) == 1:
            if isinstance(entry[0], float):
                polyline['vertex'].append(
                    (entry[0], 0.0)
                    )
            elif isinstance(entry[0], str):
                layer = entry[0]
                polyline = new_poly()
        else:
            polyline['vertex'].append(
                (entry[0], entry[1])
                )
    if polyline['vertex']:
        stack.append(polyline)
    return stack

def build_circ (data):
    def new_circ ():
        there = layer
        return {'layer': there,
                'center': [0.0, 0.0, 0.1]}
    
    layer = '0'
    stack = list()
    for line in file:
        entry = parse(line)
        circle = new_circ
        if len(entry) == 0:
            continue
        elif len(entry) == 1:
            if isinstance(entry[0], float):
                circle['center'][0] = entry[0]
            elif isinstance(entry[0], str):
                layer = entry[0]
                continue
        elif len(entry) == 2:
            circle['center'][:2] = [entry[0],
                                    entry[1]]
        else:
            circle['center'] = [entry[0],
                                entry[1],
                                entry[2]]
        stack.append(circle)
    return stack

def dxf_code (stack, mode='line'):
    text = ['  0', 'SECTION',
            '  2', 'ENTITIES']
    
    if mode == 'line':
        for line in stack:
            text.extend(
                ('  0', 'POLYLINE',
                 '  8', line['layer'])
                )
            for vertex in line['vertex']:
                text.extend(
                    ('  0', 'VERTEX',
                     '  8', line['layer'],
                     ' 10', str(vertex[0]),
                     ' 20', str(vertex[1]))
                    )
            text.extend(
                ('  0', 'SEQEND',
                 '  8', line['layer'])
                )
            
    elif mode == 'circle':
        for circle in stack:
            text.extend(
                ('  0', 'CIRCLE',
                 '  8', circle['layer'],
                 ' 10', str(circle['center'][0]),
                 ' 20', str(circle['center'][1]),
                 ' 40', str(circle['center'][2]))
                )
            
    text.extend(
        ('  0', 'ENDSEC',
         '  0', 'EOF')
        )
    return text

def getline (name=None, mode=None):
    if not name:
        name = input ('Имя файла точек: ')
    if not name.endswith('.txt'):
        name = '.'.join((name, 'txt'))
    
    if mode is None:
        print ('Пропустите строку, 0 или False, чтобы получить линию, или')
        mode = input (
            'введите 1, True или что угодно, чтобы получить кружочки: ')
    
    file = open (name, 'r')
    if mode:
        data = build_circ(file)
        text = dxf_code(data, 'circle')
    else:
        data = build_line(file)
        text = dxf_code(data, 'line')
    file.close()
    
    dxf_name = ''.join(( name[:name.rfind('.')], '.dxf' ))
    dxf = open (dxf_name, 'w')
    dxf.write('\n'.join(text))
    dxf.close()
    print ('Готово!')

__author__ = {
    'name': "Maksim Solov'ev",
    'nick': 'DamTerrion',
    'email': 'damterrion@yandex.ru',
    'github': 'https://github.com/damterrion'
    }

if __name__ == '__main__':
    getline()
