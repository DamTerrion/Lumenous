def ndxf (dxf_name):
    new = Param = Value = ''
    if dxf_name[-4:] != '.dxf' :
        dxf_name += '.dxf'
    print (dxf_name)
    dxf = open (dxf_name, 'r')
    while not (Param == '  2\n' and Value == 'ENTITIES\n'):
        # Если не начался раздел ENTITIES, файл просто просматривается
        Param = dxf.readline()
        Value = dxf.readline()
    else :
        # Если же раздел ENTITIES начался, сразу же записывается его заголовок
        new += '  0\n'+'SECTION\n'+'  2\n'+'ENTITIES\n'
        inObject = ''
        # После записи считывается следующая пара параметр-значение, чтобы было с чем работать
        Param = dxf.readline()
        Value = dxf.readline() 
        while not (Param == '  0\n' and Value == 'ENDSEC\n'):
            # Цикл работает до тех пор, пока не закончится раздел
            if Param == '  0\n' :   # Если встречается код 0, значит, начался объект,
                inObject = Value    # и требуется определить и сохранить тип объекта
            if (
                inObject == 'POLYLINE\n' or # Полилиния
                inObject == 'SOLID\n' or    # Фигура
                inObject == 'VERTEX\n' or   # Точка
                inObject == 'SEQEND\n'      # Конец последовательности точек примитива
                # Все объекты, кроме указаных, игнорируются вместе с содержимым
                ) and (
                Param == '  0\n' or # Код  0 - тип объекта
                Param == '  8\n' or # Код  8 - имя слоя
                Param == ' 10\n' or # Код 10 - координата X \
                Param == ' 20\n' or # Код 20 - координата Y  } точка 1
                Param == ' 30\n' or # Код 30 - координата Z /
                Param == ' 11\n' or # Код 11 - координата X \
                Param == ' 21\n' or # Код 21 - координата Y  } точка 2
                Param == ' 31\n' or # Код 31 - координата Z /
                Param == ' 12\n' or # Код 12 - координата X \
                Param == ' 22\n' or # Код 22 - координата Y  } точка 3
                Param == ' 32\n' or # Код 32 - координата Z /
                Param == ' 13\n' or # Код 13 - координата X \
                Param == ' 23\n' or # Код 23 - координата Y  } точка 4
                Param == ' 33\n' or # Код 33 - координата Z /
                Param == ' 40\n' or # Код 40 - начальная ширина линии
                Param == ' 41\n' or # Код 41 -  конечная ширина линии
                Param == ' 42\n' or # Код 42 - выпуклость линии в точке
                Param == ' 66\n' or # Код 66 - флаг наличия графических примитивов
                Param == ' 70\n'    # Код 70 - предположительно, замкнутость линии
                # Остальные параметры игнорируются
                ):
                if Param == ' 30\n' :
                    new += Param + '0.0\n'
                    # Положение Z в любом случае обнуляется
                else :
                    new += Param + Value
                    # В прочих случаях всё записывается "as is"
            Param = dxf.readline()
            Value = dxf.readline()
            # Ещё пока внутри ENTITIES считываются пары параметр-значение в конце итерации цикла
        else:
            # Раздел кончился, можно расслабиться и завершить данные
            new += '  0\n'+'ENDSEC\n'+'  0\n'+'EOF\n'
    dxf.close()
    dxf = open (dxf_name, 'w')    
    dxf.write(new)
    dxf.close()
    print ('Done!')
    # Запись в файл завершена, файлы закрыты, процедура завершена. EOF
    
code = ''
while True:
    code = input("Введите имя DXF-файла для обработки: ")
    if (
    code == 'quit' or
    code == 'exit' or
    code == 'выход' or
    code == 'конец'
    ): break
    ndxf (code)
