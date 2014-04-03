def dxf_read (dxf_name):
    
    if dxf_name[-4:] != '.dxf' :
        dxf_name += '.dxf'
    dxf = open (dxf_name, 'r')
    # Открываем dxf-файл на чтение
    # Если не было указано расширение файла, оно добавляется
    
    Stack = []
    Param = Value = ''
    # Инициализация переменных - стэк объектов, имя и значение параметра
    
    Allowed_objects = {'_INIT_':    (' 0', ' 8'),   # Имя и слой каждого объекта
                       'POLYLINE':  ('40', '41',    # Начальная и конечная ширина линии
                                     '70'),         # Флаг замкнутости линии
                       'SOLID':     ('10', '20',    # Координаты первой вершины
                                     '11', '21',    # Координаты второй вершины
                                     '12', '22',    # Координаты третьей вершины
                                     '13', '23'),   # Координаты четвёртой вершины
                       'VERTEX':    ('10', '20',    # Координаты точки
                                     '42')          # Выпуклость линии
                       }
    
    while not (Param == ' 2' and Value == 'ENTITIES'):
        Param = dxf.readline()[1:-1]
        Value = dxf.readline()[:-1]
        if Param == ' 0' and Value == 'EOF':
            return ('Раздел примитивов в файле не обнаружен')
            break
        # Файл пролистывается в поисках раздела примитивов
    
    while not (Param == ' 0' and Value == 'ENDSEC'):
        # Цикл, продолжающийся до тех пор, пока не закончится раздел
        if Param == ' 0' and Value in Allowed_objects:
            if Value != 'VERTEX':
                # Если обрабатываемый объект не точка, значит примитив
                # Параметры примитива сохраняются в словарь:
                Current = {'type': Value,   # Тип объекта (линия, фигура)
                           'layer': '0',    # Слой объекта
                           'point': {},     # Словарь точек со стороковыми именами
                           'vertex': 0,     # Счётчик точек полилинии - число
                           'width': None,   # Ширина полилинии
                           'closed': None   # Замкнутость полилинии
                           }
            else:
                # Если же объект - очередная точка, увеличим счётчик точек
                Current['vertex'] += 1
            
            Param = dxf.readline()[1:-1]
            Value = dxf.readline()[:-1]
            while not Param == ' 0':
                # Цикл работает до тех пор, пока не найдёт конец объекта
                if Param == ' 8': Current['layer'] = Value
                
                elif Param in ('10', '11', '12', '13') :
                    num = str(int(Param)%10+Current['vertex'])
                    if not num in Current['point']:
                        Current['point'][num] = {}
                    Current['point'][num]['x'] = Value
                    # Берётся значение координаты X точки
                    # Если точки с текущим именем не было, она создаётся
                    
                elif Param in ('20', '21', '22', '23') :
                    num = str(int(Param)%10+Current['vertex'])
                    if not num in Current['point']:
                        Current['point'][num] = {}
                    Current['point'][num]['y'] = Value
                    # Аналогично берётся значение Y точки
                    # Для фигуры точки будут '0', '1', '2', '3'
                    # Для полилинии точки будут '1', '2', '3', ...
                    
                elif Param in ('40', '41') :
                    if (Current['width'] == None or
                        Current['width'] == Value):
                        Current['width'] = Value
                        # Если значения ширины не было,
                        #  или оно совпадает с текущим, взять текущее
                    else:
                        Current['width'] = False
                        # В противном случае (было, не совпадает),
                        #  оно сразу меняется на False
                        # Линии переменной ширины не обрабатываются
                    
                elif Param == '42':
                    pass
                    # Здесь должен быть код, определяющий обработку дуги
                    
                elif (Param == '70' and
                      int(Value) == 1 and
                      Current['type'] == 'POLYLINE'):
                    Current['closed'] = True
                    # Это значит, что была принята замкнутая полилиния
                    # Важно, т.к. замкнутая линия может быть прямоугольником
                    
                Param = dxf.readline()[1:-1]
                Value = dxf.readline()[:-1]
            else:
                if Current['type'] == 'POLYLINE' and Value == 'SEQEND':
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
