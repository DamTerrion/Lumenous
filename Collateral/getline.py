def getline(name=False):
    if not name:
        name = input ('Имя файла точек: ')
        if name[-4:] != '.txt':
            name = '.'.join((name, 'txt'))
    file = open (name, 'r')
    # Производится запрос имени файла и его открытие
    
    stack = []
    # Инициализируется пустой список для точек
    for line in file:
        coords = []
        point = line.replace(',','.')
        # Все запятые (экспорт из Excel) заменяются на точки
        if '\t' in point: raw = point.split('\t')
        # Строка с координатами точки разбивается по табуляции на [X, Y]
        elif ' ' in point: raw = point.split(' ')
        # Если нет табуляции, то разбивается по пробелу
        else: raw = (point, '0.0')
        # Если нет второй координаты, она заменяется нулём
        for entry in raw:
            while entry[0] != '.' and not entry[0].isdigit(): entry = entry[1:]
            while not entry[-1].isdigit(): entry = entry[:-1]
            coords.append(entry)
            # Каждая координата проходит чистку пробельных символов
            # и записывается в новый список с "хорошими" координатами
        stack.append(coords)
        # Стэк - список точек, представленных списками координат
    file.close()
    
    form = input('Введите что-нибудь, чтобы получить кружочки: ')
    
    dxf_name = ''.join(( name[:name.rfind('.')], '.dxf' ))
    dxf = open (dxf_name, 'w')
    # Создаётся новый файл, но после первой точки в названии исходного файла
    #  ставится расширение .dxf
    try:
        text = ['  0',
                'SECTION',
                '  2',
                'ENTITIES'
                ]
        # Старт текста нового файла - описание раздела и объекта полилинии
        if form:
            # Для каждой точки из стэка генерируется код кружка
            for point in stack:
                circle = ['  0',
                          'CIRCLE',
                          '  8',
                          '0',
                          ' 10',
                          point[0],
                          ' 20',
                          point[1],
                          ' 30',
                          '0.0',
                          ' 40',
                          '0.1'
                          ]
                text.extend(circle)
        else:
            text.extend(
                ['  0',
                 'POLYLINE',
                 '  8',
                 '0'
                 ])
            # Для каждой точки из стэка генерируется код вершины
            for point in stack:
                vertex = ['  0',
                          'VERTEX',
                          '  8',
                          '0',
                          ' 10',
                          point[0],
                          ' 20',
                          point[1]
                          ]
                text.extend(vertex)
            text.extend(['  0',
                         'SEQEND',
                         '  8',
                         '0'
                         ])                     
        
        text.extend(['  0',
                     'ENDSEC',
                     '  0',
                     'EOF',
                     ''
                     ])
        # Текст завершается окончанием линии, раздела и файла
        
        dxf.write('\n'.join(text))
        # В файл записывается не сам список, а строка из элементов списка,
        #  отделённых друг от друга переводом на новую строку '\n'
    finally:
        dxf.close()
    print ('Готово!')

if __name__ == '__main__':
    getline()
