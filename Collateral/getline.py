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
        point = line.replace(',','.')
        # Все запятые (экспорт из Excel) заменяются на точки
        if '\t' in point: coords = point.split('\t')
        elif ' ' in point: coords = point.split(' ')
        else: coords = (point[:-1], '0.0')
        # Строка с координатами точки разбивается по табуляции на [X, Y]
        for entry in coords:
            entry = entry.strip()
            # Каждая координата проходит чистку пробельных символов
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
                     'EOF'
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
