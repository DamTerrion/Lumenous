from os import replace, path, mkdir, listdir
from time import ctime, time as now
from local import think, say, ask
import clearing

default_config = 'ndxf.conf'
reserve_config = {'language': 'EN',
                  'round': 3.25,
                  'backs': 'bak',
                  'clean': 'not',
                  'period': 30,
                  'report': 'yes'}

def import_config (conf_name=default_config):
    imported = dict()
    try:
        conf_file = open(conf_name)
        for line in conf_file:
            if line.find('=') > 0:
                set_name = line.partition('=')[0].strip()
                set_value = line.partition('=')[2].strip()
                if (set_name.isalnum() and
                    set_value.isalnum):
                    if set_value.isdigit(): set_value = int(set_value)
                    elif set_value == 'True': set_value = True
                    elif set_value == 'False': set_value = False
                    elif set_value == 'None': set_value = None
                    imported[set_name.lower()] = set_value
    except FileNotFoundError:
        if conf_name == default_config:
            export_config(default_config, reserve_config)
        return reserve_config
    except Exception:
        say('Unknown problem with configuration file',
            reserve_config['language'])
    finally:
        conf_file.close()
        return imported

config = import_config()
# Обязательный импорт параметров из внешнего файла

def export_config (file_name=default_config, export=config):
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
    
    conf_file.write(
        ''.join(export_text)
        )
    return True

def get_log (full_name, start_time, file_size, error=None):
    log_file = ''.join((config['backs'],
                        '/',
                        'processed.log'
                        ))    
    now_time = now()    
    t1 = '\t'*(4 - (0+len(full_name[1])) //4)
    t0 = '\t'*(5 - (3+len(full_name[0])) //4)
    
    if error:
        result = ''.join((str(error), ':', '\t',
                          full_name[1], t1, '|  ',
                          full_name[0], t0, '|  ',
                          ctime(now_time), '\n'
                          ))
    else:
        job_time = now_time - start_time
        speed  = file_size / job_time

        file_size  = str(round(file_size,  1))
        job_time = str(round(job_time, 3))
        speed  = str(round(speed,  1))
        
        t2 = '\t'*(
            4 - (
                4+
                len(job_time)+
                len(
                    think('s.', config['language'])
                    )
                )
                   //4)
        t3 = '\t'*(
            4 - (
                4+
                len(file_size)+
                len(
                    think('kB', config['language'])
                    )
                )
                    //4)
        result = ''.join((
            full_name[1],  t1, '|  ',
            full_name[0],  t0, '|  ',
            job_time, ' ', think('s.', config['language']), t2, '|  ',
            file_size, ' ', think('kB', config['language']), t3, '|  ',
            ctime(now_time), '\t','|  ',
            speed, ' kB/s', '\n'
            ))
        print('\t', think('All done in', config['language']),
              job_time,
              think('s.', config['language'])
              )
    try:
        log = open(log_file, 'a')
        log.write(result)
    except Exception:
        answer = False
    else:        
        answer = True
    finally:
        log.close()
        return answer

def adv_round (value, base=config['round']):
    if (base is False) or (base is None): return value
    # Позволяет использовать нецелые основания для округления.
    # При основании 3.50, число 0.34871 округлится до 0.3485
    # При основании 3.25, число 0.34871 округлится до 0.34875
    # При основании 3.30, число 0.34871 округлится до 0.34867
    # При основании 3.10, число 0.34871 округлится как при основании 4
    base = float(base)
    quot, tail = int(base // 1), base % 1
    inc = 1
    if tail > 0.5:
        tail = 1 - tail
    if tail > 0.1: inc = round(1 / tail)
    elif tail != 0: quot += 1
    #old_val = value
    value = round( round(value * inc, quot) / inc, quot+2)
    #if value != old_val:
    #    print (old_val, ', ', value, ', ', base)
    return value

def estimated (file_size):
    estime = (
        (file_size ** 2) * 0.000003
        )
    return round(estime, 1)

def ndxf (dxf_name, round_base=config['round'], draw=True):
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
    
    if not dxf_name.lower().endswith('.dxf'):
        dxf_name += '.dxf'
    
    try:
        dxf = open(dxf_name, 'r')
        fsize = path.getsize(dxf_name)/1024
        print(
            dxf_name+',',
            round(fsize, 2),
            think('kB', config['language']),
            '~',
            estimated(fsize),
            think('s.', config['language'])
            )
        # File opens for reading, its size saved
        ## Файл открывается для считывания, записывается его размер
    except FileNotFoundError:
        if draw:
            print(dxf_name, "-",
                  think('File not found', config['language'])
                  )
        return None
    
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
                    if round_base and int(Param[1:-1]) in range(10, 60):
                        Value = ''.join((
                            str(adv_round(float(Value[:-1]), round_base)                                ),
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

    # Name of origin file was changed, and it recreating
    ## Так как имя исходного файла сменилось, он создаётся заново
    try:
        dxf = open(dxf_name, 'w')    
        dxf.write(new)
        # Trying to save to file with exceptions trapping
        ## Попытка записи в файл с перехватом ошибок
    except Exception:
        get_log(full_name, start_tm, fsize, 'Error')
        say('Mistake was made during processing', config['language'])
        # If was found an exception, information about is logged
        ## Если возникла ошибка, то сообщение об этом выводится в лог
    else:
        get_log(full_name, start_tm, fsize)
        # If wasn't found any exceptions, process information is logged
        # Если не возникло ошибок, в лог выводится информация об обработке
    finally:
        dxf.close()

def loop (lastname=None, repeat=True):
    firsttime = True    
    quit_conditions = ('quit', 'exit',
                       'выход', 'конец', 'хватит'
                       )
    # This loop is repeatedly asking file name and operate with this file
    ## Здесь циклически спрашивается имя файла и этот файл обрабатывается
    while True:
        if not firsttime or not lastname:
            print () #Empty line before following question
            code = ask('Input name of DXF-file for processing:',
                       config['language'])
            if firsttime: firsttime = False
        else:
            code = lastname
            firsttime = False
        if not code and lastname:
            code = lastname
        else:
            lastname = code
        if code[0] == '-':
            command = code[1:]
            if command == 'all':
                for file in listdir():
                    if file.lower().endswith('.dxf'): ndxf(file)
            #elif command == 'reload':
            #    import_config()
            #    print (config)
            elif command in quit_conditions: break
            else:
                say ('Unknown command', config['language'])
        else:
            ndxf(code)
        if not repeat: break

__author__ = {
    'name': "Maksim Solov'ev",
    'nick': 'DamTerrion',
    'email': 'damterrion@yandex.ru',
    'github': 'https://github.com/damterrion'
    }

if __name__ == '__main__':
    
    if config['round']<5:
            print(
                think('Round base set at', config['language']),
                config['round']
                )

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
    
    loop('-all', False)
    # С самого начала программа отрабатывает все файлы в папке
