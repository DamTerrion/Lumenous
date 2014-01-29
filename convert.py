# О задаче данного скрипта:
# На ПФШ 116 раз промультиплицированы два модуля, каждый содержит 5 кружков разного диаметра.
# Самый маленький кружок в одном модуле совпадает с самым большим в другом модуле.
# Всего имеется 9 разных типов кружков, состоящих из разных шторок.
# Все кружки кроме самого маленького делаются с поворотом 10 градусов, самый маленький - 20 градусов.
# Все кружки кроме самого маленького разбиваются на две взаимоперпендикулярные части.
# Каждая часть каждого кружка (всего 17 штук) записывается в отдельный dxf-файл формата FP00, где 00 - порядковый номер.
# Необходимо после оптимизации каждого файла по отдельности свести их в общий с наименьшим количеством поворотов и смен шторок.

# Данный скрипт считывает каждый из 17 файлов, записывает каждую его часть, относящуюся к определённому углу в соответствующую ячейку стека
# После обработки файлов, весь стек суммируется и записывается в выходной файл.

STACK = {'A0':'', 'A1':'', 'A2':'',
         'A3':'', 'A4':'', 'A5':'',
         'A6':'', 'A7':'', 'A8':''}
X = Y = H = W = ''

for i in range(1,18):
    num = str(i)
    if i<10:
        num = '0'+num
    F1 = open('FP'+num+'.opt', 'r')
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
        STACK[A[:2]] += string
        string = F1.readline()
    F1.close()

F2 = open('result.pat', 'w')
for i in range(9):
    F2.write(STACK['A'+str(i)])
F2.write('$;\n')
F2.close()

print ('Done!')
