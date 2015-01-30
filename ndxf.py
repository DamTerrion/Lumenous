from os import replace, path, mkdir
from time import ctime, time as now
from local import say, ask
import clearing

lang = 'EN'
config = False

try:
    config = open('ndxf.conf')
    for line in config:
        if 'language' in line.lower():
            lang = line.partition('=')[2].strip()
    config.close()
except Exception:
    pass

def ndxf (dxf_name):
    new = Param = Value = ''
    round_base = False
    start_tm = now()
    
    Allowed = { '_INIT_':    (' 0', ' 8'),
                            # Name & layer for every object
                            ## Имя и слой для любого объекта
                'POLYLINE':  ('40', '41',
                            # Start & end width for polyline
                            ## Начальная и конечная ширина полилинии
                              '66', '70'),
                            # Flags for primitives & enclosed
                            ## Флаги примитивов и замкнутости
                'SOLID':     ('10', '20',
                              '11', '21',
                              '12', '22',
                              '13', '23'),
                            # Coordinates for four vertexs
                            ## Координаты четырёх вершин
                'VERTEX':    ('10', '20', '42'),  
                            # Single vertex coordinates & сovexity of line
                            ## Координаты отдельной вершины и выпуклость
                'LINE':      ('10', '20',
                              '11', '21'),
                            # Coord-s of line's start & end
                            ## Координаты начала и конца отрезка
                'ARC':       ('10', '20',
                            # Center's coord-s of arc
                            ## Координаты центра дуги
                              '40', '50', '51'),
                            # Radius, starting & ending angles
                            ## Радиус, начальный и конечный углы дуги
                'CIRCLE':    ('10', '20', '40'),
                            # Center's coord-s & radius of circle
                            ## Координаты центра и радиус окружности
                'SEQEND':    ()}
                            # End of compound object
                            ## Конец составных объектов (полилинии)
    
    if not dxf_name.endswith('.dxf'):
        dxf_name += '.dxf'
    print (dxf_name)
    
    try:
        dxf = open (dxf_name, 'r')
        fsize = str(round(path.getsize(dxf_name)/1024, 1))
        # File opens for reading, its size saved
        ## Файл открывается для считывания, записывается его размер
    except FileNotFoundError:
        say('File not found', lang)
        return False
    
    try:
        config = open('ndxf.conf')
        for line in config:
            if 'round' in line.lower():
                round_base = int(line.partition('=')[2].strip())
        config.close()
    except Exception:
        pass
    if round_base: print('round base =', round_base)
    
    while not (Param == '  2\n' and Value == 'ENTITIES\n'):
        # Till 'Entities' section starts file just viewed
        ## Если не начался раздел ENTITIES, файл просто просматривается
        Param = dxf.readline()
        Value = dxf.readline()
        
    else :
        # When 'Entites' starts it's write header
        ## Если же раздел ENTITIES начался, записывается его заголовок
        new = ''.join(('  0\n', 'SECTION\n',
                       '  2\n', 'ENTITIES\n'))
        inObject = ''
        
        while not (Param == '  0\n' and Value == 'ENDSEC\n'):
            # Loop working until section will ended
            ## Цикл работает до тех пор, пока не закончится раздел
            Param = dxf.readline()
            Value = dxf.readline()
            
            if Param == '  0\n' :
                inObject = Value[:-1]
                # If code 0 found, it mean "new object begins";
                #  it must determine and save type of new object
                ## Если встретился код 0, значит, начался объект,
                ##  и требуется определить и сохранить тип объекта

            if (inObject in Allowed and
                (Param[1:-1] in Allowed['_INIT_'] or
                 Param[1:-1] in Allowed[inObject])):
                    # If it's right couple 'object-parameter', it saving
                    ## Если рассматривается правильная пара
                    ##  объект-параметр, она записывается
                    if Roundy and int(Param[1:-1]) in range(10, 60):
                        Value = ''.join((
                            str(round(float(Value[:-1]), round_base)),
                            Value[-1]))
                    new = ''.join((new, Param, Value))
        else:
            # Section is ended, data's writing can be completed
            ## Раздел кончился, можно завершить запись данных
            new = ''.join((new, '  0\n', 'ENDSEC\n', '  0\n', 'EOF\n'))
            
    dxf.close()
    if path.exists('bak') == False :
        mkdir ('bak')
    full_name = path.split(path.abspath(dxf_name))
    try: replace (dxf_name, 'bak/'+full_name[1]+'.bak')
    except Exception:
        replace (dxf_name, dxf_name+'.bak')
        say("Can't replace this file to '/bak'!", lang)
    # Обрабатывавшийся файл <name>.dxf превращается в bak/<name>.dxf.bak
    # Если произошла ошибка (невозможно файл переместить в папку bak/),
    #  то он переименовывается в <name>.dxf.bak там, где и был, с заменой

    job_tm = str(round(now() - start_tm, 3))

    # Name of origin file was changed, and it recreating
    ## Так как имя исходного файла сменилось, он создаётся заново
    try:
        dxf = open (dxf_name, 'w')    
        dxf.write(new)
        dxf.close()
        # Trying to save to file with exceptions trapping
        ## Попытка записи в файл с перехватом ошибок
    except Exception:
        log = open ('bak/processed.log', 'a')
        log.write('\t'.join(('Error',
                             full_name[1], '|',
                             full_name[0], '|',
                             ctime(now()), '\n'
                             )))
        log.close()
        say('Mistake was made during processing', lang)
        # If was found an exception, it's logging to log
        ## Если возникла ошибка, то сообщение об этом выводится в лог
    else:
        t1 = '\t'*(4 - (0+len(full_name[1])) //4)
        t0 = '\t'*(5 - (3+len(full_name[0])) //4)
        t2 = '\t'*(4 - (3+len(job_tm+' s.')) //4)
        t3 = '\t'*(4 - (3+len(fsize+' kB.')) //4)
        log = open ('bak/processed.log', 'a')
        log.write(''.join((full_name[1],  t1, '|  ',
                           full_name[0],  t0, '|  ',
                           job_tm, ' s.', t2, '|  ',
                           fsize, ' kB.', t3, '|  ',
                           ctime(now()), '\n'
                           ))
                  )
        log.close()        
        # If wasn't found any exceptions, processe's information logging
        # Если не возникло ошибок, в лог выводится информация об обработке
        
        print(say('All done in', lang, 'np'), job_tm, say('s.', lang, 'np'))


__author__ = 'Maksim "DamTerrion" Solov\'ev'


if __name__ == '__main__':
    need = ask('Activate clearing? (Yes/Not/Days)', lang)
    clearing.call(need)
    # Garbage cleaning from user's choice
    #  if this script is main script
    ## Подчистка мусора на выбор пользователя,
    ##  если этот скрипт запущен как основной,
    ##  а не импортирован из другого скрипта.
    lastname = False
 
while __name__ == '__main__':
    # Loop working only if it is a main script
    ## Цикл выполняется, если это главный скрипт,
    ##  а не импортированный
    code = ask('Input name of DXF-file for processing:', lang)
    if not code and lastname:
        code = lastname
    else:
        lastname = code
    if code.lower() in ('quit', 'exit', 'выход', 'конец', 'хватит') : break
    ndxf(code)
