from os import replace, path, mkdir
import clearing

def ndxf (dxf_name):
    new = Param = Value = ''
    
    if dxf_name[-4:] != '.dxf' :
        dxf_name += '.dxf'
    print (dxf_name)
    
    try:
        dxf = open (dxf_name, 'r')
        # Файл открывается для считывания
    except FileNotFoundError:
        print ('Такой файл не найден.')
        return False
    
    Allowed = { '_INIT_':    (' 0', ' 8'),      # Имя и слой каждого объекта
                'POLYLINE':  ('40', '41',       # Начальная и конечная ширина линии
                              '66', '70'),      # Флаг примитивов и замкнутость линии
                'SOLID':     ('10', '20',       # Координаты первой вершины
                              '11', '21',       # Координаты второй вершины
                              '12', '22',       # Координаты третьей вершины
                              '13', '23'),      # Координаты четвёртой вершины
                'VERTEX':    ('10', '20',       # Координаты точки
                              '42'),            # Выпуклость линии
                'LINE':      ('10', '20',       # Координаты начала отрезка
                              '11', '21',),     # Координаты конца  отрезка
                'ARC':       ('10', '20',       # Координаты центра дуги
                              '40', '50', '51'),# Радиус, начальный и конечный углы дуги
                'CIRCLE':    ('10', '20',       # Координаты центра
                              '40'),            # Радиус окружности
                'SEQEND':    ()}                # Объект окончания полилинии
    
    while not (Param == '  2\n' and Value == 'ENTITIES\n'):
        # Если не начался раздел ENTITIES, файл просто просматривается
        Param = dxf.readline()
        Value = dxf.readline()
        
    else :
        # Если же раздел ENTITIES начался, сразу же записывается его заголовок
        new += '  0\n'+'SECTION\n'+'  2\n'+'ENTITIES\n'
        inObject = ''
        
        while not (Param == '  0\n' and Value == 'ENDSEC\n'):
            # Цикл работает до тех пор, пока не закончится раздел
            Param = dxf.readline()
            Value = dxf.readline()
            
            if Param == '  0\n' :       # Если встречается код 0, значит, начался объект,
                inObject = Value[:-1]   # и требуется определить и сохранить тип объекта

            if (inObject in Allowed and
                (Param[1:-1] in Allowed['_INIT_'] or
                 Param[1:-1] in Allowed[inObject])):
                    # Если рассматривается правильная пара объект-параметр, она записывается
                    new += Param + Value
        else:
            # Раздел кончился, можно расслабиться и завершить запись данных
            new += '  0\n'+'ENDSEC\n'+'  0\n'+'EOF\n'
            
    dxf.close()
    if path.exists('bak') == False :
        mkdir ('bak')      
    replace (dxf_name, 'bak/'+dxf_name+'.bak')
    # Обрабатывавшийся файл <name>.dxf превращается в bak/<name>.dxf.bak

    # Так как имя исходного файла сменилось, создаётся новый файл с исходным именем
    dxf = open (dxf_name, 'w')    
    dxf.write(new)
    dxf.close()
    print ('Well done!')
    # Запись в файл завершена, файлы закрыты, процедура завершена. EOF
    
code = ''
clearing.bak(45)
# Подчистка мусора - удаляются все bak-файлы старше 45 дней

while True :
    code = input("Введите имя DXF-файла для обработки: ")
    if code in ('quit', 'exit', 'выход', 'конец') : break
    ndxf (code)
    # Цикл повторяется до тех пор, пока в качестве имени файла
    # не будет указано ключевое слово: "exit", "quit", "выход" или "конец"
