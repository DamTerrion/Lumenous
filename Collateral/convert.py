from os.path import exists

def prepare (FILES):
    STACK = {}
    X = Y = H = W = ''
    for name in FILES:
        F1 = open(name, 'r')
        string = F1.readline()
        while not '$' in string :
            
            X1 = string.find('X')
            Y1 = string.find('Y')
            H1 = string.find('H')
            W1 = string.find('W')
            A1 = string.find('A')
            A2 = string.find(';')
            
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

            if X1 > -1: X = string[X1:X2]
            if Y1 > -1: Y = string[Y1:Y2]
            if H1 > -1: H = string[H1:H2]
            if W1 > -1: W = string[W1:W2]

            if A1 > -1:
                A = string[A1:A2]
                string = X+Y+H+W+A+';\n'

            if not A in STACK:
                STACK[A]=''
                # Если угла не было в стэке, он добавляется с пустым полем
            STACK[A] += string
            string = F1.readline()
        F1.close()
    return STACK

def combine (STACK, result_name=None):
    while not result_name:
        result_name = input('Имя выходного файла: ')
        if exist(result_name):
            confirming = input('Подтверждаете перезапись? ')
            if confirming.lower() in ('n', 'no', 'not'
                                      'н', 'не', 'нет'):
                result_name = None
    F2 = open(name, 'w')
    for item in sorted(STACK):
        F2.write(STACK[item])
    F2.write('$;\n')
    F2.close()
    print ('Done!\n')

def read_names ():
    name = False
    NAMES = []
    count = 0
    while not name in ('quit', 'exit', 'enought',
                       'конец', 'выход', 'хватит'):
        name = input('Введите имя файла: ')
        if not name in ('quit', 'exit', 'enought',
                        'конец', 'выход', 'хватит'):
            if exists(name): NAMES.append(name)
            count += 1
        else: break
    if count:
        print('Считано имён: %i/%i' %(len(NAMES), count))
    return NAMES, count

def loop ():
    while True:
        NAMES, count = read_names()
        if not count: break
        DATA = prepare(NAMES)
        combine(DATA)

if __name__ == '__main__':
    loop()
