from math import atan2, degrees

def clear_objects ():
    return {
        'type'  : None, # Тип объекта (линия, фигура)
        'layer' : '0',  # Слой объекта
        'points': {},   # Словарь точек со стороковыми именами
        'vertex': 0,    # Счётчик точек полилинии - число
        'width' : None, # Ширина полилинии
        'closed': None  # Замкнутость полилинии
        }
precision = -4


def by4points (rectangle, is_solid, prec=-4):
    if is_solid:
        p1 = rectangle['points']['0']
        p2 = rectangle['points']['1']
        p3 = rectangle['points']['2']
        p4 = rectangle['points']['3']
    else:
        p1 = rectangle['points']['1']
        p2 = rectangle['points']['2']
        p3 = rectangle['points']['4']
        p4 = rectangle['points']['3']
    # В фигуре порядок точек не такой, как в прямоугольнике
    # Чтобы это исправить, третья и четвёртая точки меняются местами
    # Кроме того, отличается генерация имён точек (см. dxf_read дальше)
    
    l1, l2 = p1 - p2, p3 - p4
    w1, w2 = p1 - p3, p2 - p4
    c = (p1 + p2 + p3 + p4) / 4
    if (abs(l1 - l2) < 10 ** prec and
        abs(w1 - w2) < 10 ** prec and
        l1.real/l1.imag - w1.imag/w1.real < 10 ** prec):
        # Проверка координат на точность; сравнение с нулём малополезно,
        #  потому что координаты всегда могут быть не очень точны
        x = c.real * 1000
        y = c.imag * 1000
        l = abs (l1) * 1000
        w = abs (w1) * 1000
        a = degrees( atan2(l1.real, l1.imag) ) * 10
        layer = rectangle['layer']
        return Line(x, y, l, w, a, layer)
        # формат Line хранит значения в мкм и 0.1 градуса

def from_poly (polyline, prec=-4):
    if not polyline['width']:
        if ( polyline['vertex'] == 4 and
             polyline['closed'] ):
            return by4points(polyline, False, prec)
        else: return False
    sStack = []
    prev = False
    for point in sorted(polyline['points']):
        if not prev:
            prev = point
            continue
        c = (point + prev) / 2
        v = point - prev
        
        x = c.real * 1000
        y = c.imag * 1000
        l = abs(v) * 1000
        w = polyline['width']
        a = degrees( atan2(v.real, v.imag) ) * 10
        layer = polyline['layer']
        sStack.append( Line(x, y, l, w, a, layer) )
    return sStack


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
                # Если обрабатываемый объект не точка, значит - примитив
                # Параметры примитива сохраняются в словарь:
                Current = clear_objects()
                Current['type'] = Value
            else:
                # Если же объект - очередная точка, увеличим счётчик
                # Это важно для записи точек полилинии и прямоугольника
                Current['vertex'] += 1
            
            Param = dxf.readline()[1:-1]
            Value = dxf.readline()[:-1]
            while not Param == ' 0':
                # Цикл работает до тех пор, пока не найдёт конец объекта
                if Param == ' 8': Current['layer'] = Value
                
                elif Param in ('10', '11', '12', '13') :
                    num = str(int(Param)%10+Current['vertex'])
                    if not num in Current['points']:
                        Current['points'][num] = {}
                    Current['points'][num]['x'] = Value
                    # Берётся значение координаты X точки
                    # Если точки с текущим именем не было, она создаётся
                    
                elif Param in ('20', '21', '22', '23') :
                    num = str(int(Param)%10+Current['vertex'])
                    if not num in Current['points']:
                        Current['points'][num] = {}
                    Current['points'][num]['y'] = Value
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
                    
                elif all(Param == '70', int(Value) == 1,
                         Current['type'] == 'POLYLINE'):
                    Current['closed'] = True
                    # Это значит, что была принята замкнутая полилиния
                    # Важно: замкнутая линия может быть прямоугольником
                    # А прямоугольник обрабатывается почти как фигура
                    
                Param = dxf.readline()[1:-1]
                Value = dxf.readline()[:-1]
            else:
                if Current['type'] == 'POLYLINE' and Value == 'SEQEND':
                    new = from_poly(Current, precision)
                    if new: Stack.extend(new)
                    # Полилиния может содержать несколько объектов
                    # Поэтому функция from_poly возращает стек,
                    #  за счёт которого общий стек расширяется
                    
                elif Current['type'] == 'SOLID':
                    new = by4points(Current, True, precision)
                    if new: Stack.append(new)
                    # Фигура содержит только один объект
                    # Его можно просто добавить в общий стэк

    dxf.close()
    return Stack
    print ('Done!')
    # Запись в файл завершена, файлы закрыты, процедура завершена. EOF
