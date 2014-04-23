from math import atan2, degrees
from SimpleLine import Line

def clear_objects ():
    return {
        'type'  : None, # Тип объекта (линия, фигура)
        'layer' : '0',  # Слой объекта
        'points': {},   # Словарь точек со стороковыми именами
        'vertex': 0,    # Счётчик точек полилинии - число
        'width' : None, # Ширина полилинии
        'closed': None, # Замкнутость полилинии
        'colour': None  # Цвет объекта, если он задан явно
        }
precision = -4


def by4points (rectangle, is_solid, precision=-4):
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
    if ( abs(l1 - l2) < 10 ** precision and
         abs(w1 - w2) < 10 ** precision and
         l1.real/l1.imag - w1.imag/w1.real < 10 ** precision ):
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
    else: return False

def from_poly (polyline, precision=-4):
    if not polyline['width']:
        if ( polyline['vertex'] == 4 and
             polyline['closed'] ):
            return [by4points(polyline, False, precision)]
            # from_poly, в отличие от by4points должна вернуть список
        else: return False
    sStack = []
    prev = False
    for point in sorted(polyline['points']):
        last = polyline['points'][point]
        if not prev:
            prev = last
            continue
        c = (last + prev) / 2
        v = last - prev
        if abs(v) < 10 ** precision : continue
        # Если точки совпадают, то их пара не обрабатывается
        
        x = c.real * 1000
        y = c.imag * 1000
        l = abs(v) * 1000
        w = polyline['width']
        a = degrees( atan2(v.real, v.imag) ) * 10
        layer = polyline['layer']
        sStack.append( Line(x, y, l, w, a, layer) )
    return sStack
    # Важно! Функция возвращает не один объект, а список объектов

def to_Line (stack, precision=-4):
    Result = []
    for item in stack:
        if item['type'] == 'POLYLINE':
            new = from_poly(item, precision)
            if new:
                Result.extend(new)
                print (new)
            # Полилиния может содержать несколько объектов
            # Поэтому функция from_poly возращает список,
            #  за счёт которого общий стек расширяется
        elif item['type'] == 'SOLID':
            new = by4points(item, True, precision)
            if new:
                Result.append(new)
                print (new)
            # Фигура содержит только один объект
            # Его можно просто добавить в общий стэк
    return Result

def to_pat (stack):
    Result = ''
    for item in stack:
        new = item.pat()
        if not 'Error' in new:
            Result += new['out']
    return Result


def dxf_read (dxf_name=False):
    listened_dxf = ''
    
    if not dxf_name:
        dxf_name = input ('Введите имя файла: ')
    
    if dxf_name[-4:] != '.dxf' :
        dxf_name += '.dxf'
        # Если не было указано расширение файла, оно добавляется

    try:
        dxf = open (dxf_name, 'r')
        # Открываем dxf-файл на чтение c перехватом ошибок
    except FileNotFoundError:
        print ('Файл не найден.')
        return dxf_read(False)
    
    Stack = []
    Param = 0
    Value = ''
    # Инициализация переменных - стэк объектов, имя и значение параметра
    
    Allowed_objects = {'POLYLINE',
                       'SOLID',
                       'VERTEX'
                       }
    
    while not (Param == 2 and Value == 'ENTITIES'):
        Param = int(dxf.readline())
        Value = dxf.readline()[:-1]
        if Param == 0 and Value == 'EOF':
            print ('Раздел примитивов в файле не обнаружен')
            return False
            break
        # Файл пролистывается в поисках раздела примитивов
    
    while not (Param == 0 and Value == 'EOF'):
        # Цикл, продолжающийся до тех пор, пока не закончится раздел
        if Param == 0 and Value in Allowed_objects:
            if Value != 'VERTEX':
                # Если обрабатываемый объект не точка,
                #  необходимо сохранить предыдущий примитив.
                try: Stack.append(Current)
                except UnboundLocalError: pass
                # Так же нужно инициировать запись нового объекта
                Current = clear_objects()
                Current['type'] = Value
            else:
                Current['vertex'] += 1                  
                # Если же объект - очередная точка, увеличим счётчик
                # Это важно для записи точек полилинии и прямоугольника
            Param = int(dxf.readline())
            Value = dxf.readline()[:-1]
            while not Param == 0:
                # Цикл работает до тех пор, пока не найдёт конец объекта
                if Param == 8:
                    Current['layer'] = Value
                
                elif Param in (10, 11, 12, 13) :
                    num = str(Param%10+Current['vertex'])
                    if not num in Current['points']:
                        Current['points'][num] = 0j
                    Current['points'][num] += complex (float(Value), 0)
                    # Берётся значение координаты X точки
                    # Если точки с текущим именем не было, она создаётся
                    
                elif Param in (20, 21, 22, 23) :
                    num = str(Param%10+Current['vertex'])
                    if not num in Current['points']:
                        Current['points'][num] = 0j
                    Current['points'][num] += complex (0, float(Value))
                    # Аналогично берётся значение Y точки
                    # Для фигуры точки будут '0', '1', '2', '3'
                    # Для полилинии точки будут '1', '2', '3', ...
                    
                elif Param in (40, 41) :
                    if (Current['width'] == None or
                        Current['width'] == float(Value)):
                        Current['width'] = float(Value)
                        # Если значения ширины не было,
                        #  или оно совпадает с текущим, взять текущее
                    else:
                        Current['width'] = False
                        # В противном случае (было, не совпадает),
                        #  оно сразу меняется на False
                        # Линии переменной ширины не обрабатываются
                    
                elif Param == 42:
                    pass
                    # Здесь должен быть код, определяющий обработку дуги
                    
                elif (Param == 70 and int(Value) == 1 and
                      Current['type'] == 'POLYLINE'):
                    Current['closed'] = True
                    # Это значит, что была принята замкнутая полилиния
                    # Важно: замкнутая линия может быть прямоугольником
                    # А прямоугольник обрабатывается почти как фигура
                    
                Param = int(dxf.readline())
                Value = dxf.readline()[:-1]
            # Цикл обработки объекта завершается здесь.
        Param = dxf.readline()
        Value = dxf.readline()[:-1]
        if Param != '': Param = int(Param)
        else: break
        # Почему-то условия окончания цикла по ENDSEC и EOF не работают,
        #  и программа продолжает извлекать пустые строки из файла.
        # Я в большом замешательстве, и не понимаю почему это так.
    
    dxf.close()
    return Stack
# Здесь кончается функция read_dxf
    
if __name__ == '__main__':
    name = input('Имя файла: ')
    first = dxf_read(name)
    print (first)
    second = to_Line(first)
    print (second)
    third = to_pat(second)
    print (second)
    pat = open (name+'.pat', 'w')
    pat.write(third)
    pat.close()
