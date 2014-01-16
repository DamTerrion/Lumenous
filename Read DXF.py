def dxf_read (dxf_name):
    Stack = {'0':()}
    Param = Value = ''
    
    Allowed_objects = {'_INIT_':    (' 0', ' 8'),
                       'POLYLINE':  ('40', '41',
                                     '66', '70'),
                       'SOLID':     ('10', '20',
                                     '11', '21',
                                     '12', '22',
                                     '13', '23'),
                       'VERTEX':    ('10', '20', '42'),
                       'SEQEND':    ()}

    if dxf_name[-4:] != '.dxf' :
        dxf_name += '.dxf'
    dxf = open (dxf_name, 'r')
    
    while not (Param == ' 2' and Value == 'ENTITIES'):
        Param = dxf.readline()[1:-1]
        Value = dxf.readline()[:-1]
        if Param == ' 0' and Value == 'EOF':
            print ('ENTITIES SECTION NOT FOUND')
            break
    else :
        Param = dxf.readline()[1:-1]
        Value = dxf.readline()[:-1]
        Current = {'type': None, 'points': 0}
        while not (Param == ' 0' and Value == 'ENDSEC'):
            if (Param == ' 0' and Value in Allowed_objects):
                if Value != 'VERTEX':
                    Current['type'] = Value
                    counter = 0
                else:
                    counter += 1
                while not Param == ' 0':
                    if Param == ' 8': Layer = Value
                    elif Param == '10' : Current[str(counter)]['x'] = Value
                    elif Param == '20' : Current[str(counter)]['y'] = Value
                    elif Param in ('11', '12', '13') :
                        counter = max(counter, int(Param)%10+1)
                        Current[str(int(Param)%10+1)]['x'] = Value
                    elif Param in ('21', '22', '23') :
                        counter = max(counter, int(Param)%10+1)
                        Current[str(int(Param)%10+1)]['y'] = Value

            Param = dxf.readline()
            Value = dxf.readline()
            # Ещё пока внутри ENTITIES считываются пары параметр-значение в конце итерации цикла
        else:
            # Раздел кончился, можно расслабиться и завершить запись данных
            new += '  0\n'+'ENDSEC\n'+'  0\n'+'EOF\n'
    dxf.close()
    dxf = open (dxf_name, 'w')    
    dxf.write(new)
    dxf.close()
    print ('Well done!')
    # Запись в файл завершена, файлы закрыты, процедура завершена. EOF
