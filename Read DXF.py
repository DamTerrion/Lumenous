def dxf_read (dxf_name):
    
    if dxf_name[-4:] != '.dxf' :
        dxf_name += '.dxf'
    dxf = open (dxf_name, 'r')
    
    Stack = []
    Param = Value = ''
    
    Allowed_objects = {'_INIT_':    (' 0', ' 8'),       # Имя и слой каждого объекта
                       'POLYLINE':  ('40', '41',        # Начальная и конечная ширина линии
                                     '66', '70'),       # Флаг примитивов и замкнутость линии
                       'SOLID':     ('10', '20', '30',  # Координаты первой вершины
                                     '11', '21', '31',  # Координаты второй вершины
                                     '12', '22', '32',  # Координаты третьей вершины
                                     '13', '23', '33'), # Координаты четвёртой вершины
                       'VERTEX':    ('10', '20', '30',  # Координаты точки
                                     '42'),             # Выпуклость линии
                       'SEQEND':    ()}
    
    while not (Param == ' 2' and Value == 'ENTITIES'):
        Param = dxf.readline()[1:-1]
        Value = dxf.readline()[:-1]
        if Param == ' 0' and Value == 'EOF':
            return ('ENTITIES SECTION NOT FOUND')
            break
    Current = {'type': None}
    while not (Param == ' 0' and Value == 'ENDSEC'):
        # Цикл, продолжающийся до тех пор, пока не закончится раздел
        if (Param == ' 0' and Value in Allowed_objects):
            if Value != 'VERTEX':
                Current['type'] = Value
                counter = 0
            Param = dxf.readline()[1:-1]
            Value = dxf.readline()[:-1]                
            while not Param == ' 0':
                # Цикл работает до тех пор, пока не найдёт конец объекта
                if Param == ' 8': Current['Layer'] = Value
                elif Param == '10' : Current[str(counter)]['x'] = Value
                elif Param == '20' : Current[str(counter)]['y'] = Value
                elif Param in ('11', '12', '13') :
                    counter = max(counter, int(Param)%10+1)
                    Current[str(int(Param)%10+1)]['x'] = Value
                elif Param in ('21', '22', '23') :
                    counter = max(counter, int(Param)%10+1)
                    Current[str(int(Param)%10+1)]['y'] = Value
                elif Param in ('40', '41') :
                    Current['width'][str(int(Param)%10)] = Value
                    # Параметры, соответстветствующие ширине линии
                elif Param == '42':
                    pass
                    # Здесь должен быть код, определяющий обработку дуги
                elif (Param == '70' and
                      int(Value) == 1 and
                      Current['type'] == 'POLYLINE'):
                    Current['closed'] = True
                    # Это значит, что была принята замкнутая полилиния
                    
                Param = dxf.readline()[1:-1]
                Value = dxf.readline()[:-1]
            else:
                if Value == 'VERTEX':
                    counter += 1
                    # Если последним обработанным объектом является точка,
                    # количество точек увеличивается на одну, цикл перезапускается.
                    # Если объектом была не точка, происходит обработка.
                elif Current['type'] == 'POLYLINE':
                    pass
                    # Здесь должен быть код генерации объекта из полилинии
                    # ВКЛЮЧАЯ ДУГИ И ПРЯМОУГОЛЬНИКИ!
                elif Current['type'] == 'SOLID':
                    pass
                    # Здесь должен быть код генерации объекта из фигуры


    dxf.close()
    return Stack
    print ('Done!')
    # Запись в файл завершена, файлы закрыты, процедура завершена. EOF
