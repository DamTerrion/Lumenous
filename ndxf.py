from os import replace, path, mkdir
from time import ctime, time as now
from local import say, ask
import clearing

config = {'language': 'EN',
          'round': False,
          'backs': 'bak',
          'clean': 'not',
          'period': 30,
          'report': 'yes'}

def export_config (file_name='ndxf.conf', export=config):
    export_file = open(file_name, 'w')
    export_text = ['-= nDXF configuration settings =-', '\n']
    
    export_text.extend(('\n', '- main -', '\n'))
    for entry in ('language', 'round', 'back'):
        if entry in export:
            export_text.extend((entry, ' = ', export[entry], '\n'))
    
    export_text.extend(('\n', '- cleaning -', '\n'))
    for entry in ('clean', 'period', 'report'):
        if entry in export:
            export_text.extend((entry, ' = ', export[entry], '\n'))
    
    configuration_file.write(
        ''.join(configuration_text)
        )

try:
    configuration_file = open('ndxf.conf')
    for line in configuration_file:
        if line.find('=') > 0:
            sett_name = line.partition('=')[0].strip()
            sett_value = line.partition('=')[2].strip()
            if (sett_name.isalnum() and
                sett_value.isalnum):
                if sett_value.isdigit(): sett_value = int(sett_value)
                elif sett_value == 'True': sett_value = True
                elif sett_value == 'False': sett_value = False
                config[sett_name.lower()] = sett_value
except Exception:
    print ('Problem with configuration file')    
finally:
    configuration_file.close()

def ndxf (dxf_name, rounds=config['round'], draw=False):
    new = Param = Value = ''
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
    
    try:
        dxf = open (dxf_name, 'r')
        print(dxf_name)
        fsize = path.getsize(dxf_name)/1024
        # File opens for reading, its size saved
        ## Файл открывается для считывания, записывается его размер
    except FileNotFoundError:
        if draw:
            print(dxf_name)
            say('File not found', config['language'])
        return None
    
    if rounds: print('round base =', rounds)
    
    '''
    block_list = {'no_name': list()}
    in_block = False
    '''
    
    while not (Param == '  2\n' and Value == 'ENTITIES\n'):
        # Till 'Entities' section starts file just viewed
        ## Если не начался раздел ENTITIES, файл просто просматривается
        Param = dxf.readline()
        Value = dxf.readline()

        '''
        if Param == '  0\n' and Value == 'BLOCK\n':
            in_block = 'no_name'
        if in_block:
            block_list[in_block].append((Param, Value))
        if in_block == 'no_name' and Param == '  2\n':
            ## Когда блок получает имя, все его данные перезаписываются
            ##  в новую ячейку, а ячейка 'no_name' очищается
            in_block = Value[:-1]
            block_list[in_block] = list().extend(block_list['no_name'])
            block_list['no_name'] = list()
        '''
        
    else :
        # When 'Entites' starts it's write header
        ## Если же раздел ENTITIES начался, записывается его заголовок
        new = '\n'.join(('  0', 'SECTION',
                         '  2', 'ENTITIES',
                         ''))
        inObject = ''
        
        insertion_found = False
        
        while not (Param == '  0\n' and Value == 'ENDSEC\n'):
            # Loop working until section will ended
            ## Цикл работает до тех пор, пока не закончится раздел
            Param = dxf.readline()
            Value = dxf.readline()
            
            if Value == 'INSERT\n' and not insertion_found:
                say('Insertion!', config['language'])
            
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
                    if rounds and int(Param[1:-1]) in range(10, 60):
                        Value = ''.join((
                            str(round(float(Value[:-1]), rounds)),
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
        say("Can't replace this file to '/bak'!", config['language'])
    # Обрабатывавшийся файл <name>.dxf превращается в bak/<name>.dxf.bak
    # Если произошла ошибка (невозможно файл переместить в папку bak/),
    #  то он переименовывается в <name>.dxf.bak там, где и был, с заменой

    job_tm = now() - start_tm
    speed  = fsize / job_tm
    
    fsize  = str(round(fsize,  1))
    job_tm = str(round(job_tm, 3))
    speed  = str(round(speed,  1))

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
        say('Mistake was made during processing', config['language'])
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
                           ctime(now()), '\t','|  ',
                           speed, 'kB/s', '\n'
                           ))
                  )
        log.close()        
        # If wasn't found any exceptions, processe's information logging
        # Если не возникло ошибок, в лог выводится информация об обработке
        
        print(say('All done in', config['language'], 'np'),
              job_tm, say('s.', config['language'], 'np'))

def loop (lastname=None):
    # This loop is repeatedly asking file name and operate with this file
    ## Здесь циклически спрашивается имя файла и этот файл обрабатывается
    while True:
        code = ask('Input name of DXF-file for processing:', config['language'])
        if not code and lastname:
            code = lastname
        else:
            lastname = code
        quit_conditions = ('quit', 'exit', 'выход', 'конец', 'хватит')
        if code.lower() in quit_conditions: break
        ndxf(code, draw=True)

__author__ = 'Maksim "DamTerrion" Solov\'ev'


if __name__ == '__main__':
    if config['clean'].lower() == 'manual':
        clean_need = ask('Activate clearing? (Yes/Not/Days)',
                         config['language'])
    elif (config['clean'].lower() in ('auto', 'yes', 1) and
          'period' in config):
        clean_need = config['period']
    elif config['clean'].lower() in ('not', 'no', 0):
        clean_need = False
    clearing.call(clean_need)
    # Garbage cleaning from user's choice
    #  if this script is main script
    ## Подчистка мусора на выбор пользователя,
    ##  если этот скрипт запущен как основной,
    ##  а не импортирован из другого скрипта.
    
    loop()
