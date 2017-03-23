from os.path import exists

def num (entry, roundy=3):
    return str(round(float(entry.strip()), roundy))

def Vertex (data):
    x, y = num(data[4]), num(data[6])
    return ''.join((x, ', ', y))

def getFromDxf (dxf_file):
    stack, result = list(), list()
    for line in dxf_file:
        stack.append(line.strip())
    i = 0
    first = True
    while i < len(stack):
        if stack[i] == 'POLYLINE' and not first:
            result.append('\n')
            i += 3
        if stack[i] == 'VERTEX':
            first = False
            coords = Vertex(stack[i:i+7])
            result.append(coords)
            i += 7
        i += 1
    return '\n'.join(result)

def openfile (name=None):
    while not name:
        name = input('Введите имя файла: ')
        if not exists(name): name = None
    data = open(name, 'r')
    stack = getFromDxf(data)
    data.close()
    result = open(name+'.txt', 'w')
    result.write(stack)
    result.close()
    print('Готово.')
    return name

def loop (name=None):
    while True:
        name = openfile(name)
        if name in ('quit', 'exit', 'enought',
                    'конец', 'выход', 'хватит'): break
        name = None

if __name__ == '__main__':
    loop()
