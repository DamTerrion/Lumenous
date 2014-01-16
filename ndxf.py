def ndxf (dxf_name):
    new = Param = Value = ''
    
    if dxf_name[-4:] != '.dxf' :
        dxf_name += '.dxf'
    dxf = open (dxf_name, 'r')
    # Файл открыт и готов к считыванию
    
    Allowed_objects = {'_INIT_':    (' 0', ' 8'),       # Имя и слой каждого объекта
                       'POLYLINE':  ('40', '41',        # Начальная и конечная ширина линии
                                     '66', '70'),       # Флаг примитивов и замкнутость линии
                       'SOLID':     ('10', '20',        # Координаты первого угла
                                     '11', '21',        # Координаты второго угла
                                     '12', '22',        # Координаты третьего угла
                                     '13', '23'),       # Координаты четвёртого угла
                       'VERTEX':    ('10', '20', '42'), # Координаты точки и "выпуклость" линии
                       'SEQEND':    ()}                 # Объект окончания полилинии
    
    while not (Param == '  2\n' and Value == 'ENTITIES\n'):
        Param = dxf.readline()
        Value = dxf.readline()
        # Если не начался раздел ENTITIES, файл просто просматривается
        
    else :
        new += '  0\n'+'SECTION\n'+'  2\n'+'ENTITIES\n'
        # Если же раздел ENTITIES начался, сразу же записывается его заголовок
        
        Param = dxf.readline()
        Value = dxf.readline() 
        # После записи считывается следующая пара параметр-значение, чтобы было с чем работать
        
        inObject = ''
        while not (Param == '  0\n' and Value == 'ENDSEC\n'):
            # Цикл работает до тех пор, пока не закончится раздел
            if Param == '  0\n':        # Если встречается код 0, значит, начался объект,
                inObject = Value[:-1]   # и требуется определить и сохранить тип объекта
            if (inObject in Allowed_objects and
                (Param[1:-1] in Allowed_objects['_INIT_'] or
                 Param[1:-1] in Allowed_objects[inObject])):
                # Если параметр принадлежит правильному объекту
                # Если это правильный параметр для этого объекта
                # В таком случае пара параметр-значение записывается
                new += Param + Value
                
            Param = dxf.readline()
            Value = dxf.readline()
            # Новая пара параметр-значение считывается в конце итерации цикла, пока ещё в ENTITIES
        else:
            # Раздел кончился, можно расслабиться и завершить данные
            new += '  0\n'+'ENDSEC\n'+'  0\n'+'EOF\n'
            
    dxf.close()
    dxf = open (dxf_name, 'w')    
    dxf.write(new)
    dxf.close()
    print ('Done!')
    # Запись в файл завершена, файлы закрыты, процедура завершена. EOF

exit_code = ('exit', 'quit', 'конец', 'выход')
while True:
    code = input("Введите имя DXF-файла для обработки: ")
    if code in exit_code: break
    ndxf (code)
