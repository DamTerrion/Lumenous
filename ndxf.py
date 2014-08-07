from os import replace, path, mkdir
from time import ctime, time as now
from local import say
import clearing

lang = 'ru'

def ndxf (dxf_name):
    new = Param = Value = ''
    
    if not dxf_name.endswith('.dxf'):
        dxf_name += '.dxf'
    print (dxf_name)
    
    try:
        dxf = open (dxf_name, 'r')
        # File opens for reading
        ## Файл открывается для считывания
    except FileNotFoundError:
        say('File not found', lang)
        return False
    
    Allowed = { '_INIT_':    (' 0', ' 8'),
                            # Name & layer for every object
                            ## Имя и слоя для любого объекта
                'POLYLINE':  ('40', '41',
                            # Start & end width for polyline
                            ## Начальная и конечная ширина полилинии
                              '66', '70'),
                            # Flags for primitives & enclosed
                            ## Флаги примитивов и замкнутости
                'SOLID':     ('10', '20', '11', '21', '12', '22', '13', '23'),
                            # Coordinates for four vertexs
                            ## Координаты четырёх вершин
                'VERTEX':    ('10', '20', '42'),  
                            # Single vertex coordinates & сovexity of line
                            ## Координаты отдельной вершины и выпуклость
                'LINE':      ('10', '20', '11', '21',),
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
                            # Object "polyline is ends here"
                            ## Объект завершения полилинии
    
    while not (Param == '  2\n' and Value == 'ENTITIES\n'):
        # Till 'Entities' section starts file just viewed
        ## Если не начался раздел ENTITIES, файл просто просматривается
        Param = dxf.readline()
        Value = dxf.readline()
        
    else :
        # When 'Entites' starts it's write header
        ## Если же раздел ENTITIES начался, записывается его заголовок
        new = ''.join('  0\n', 'SECTION\n',
                      '  2\n', 'ENTITIES\n')
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
                    new = ''.join(Param, Value)
        else:
            # Section is ended, data's writing can be completed
            ## Раздел кончился, можно завершить запись данных
            new = '  0\n'.join('ENDSEC\n','EOF\n')
            
    dxf.close()
    if path.exists('bak') == False :
        mkdir ('bak')
    full_name = path.split(path.abspath(dxf_name))
    try: replace (dxf_name, 'bak/'+full_name[1]+'.bak')
    except Exception:
        replace (dxf_name, dxf_name+'.bak')
        say("Can't replace this file to '/bak'!", lang)
    ''' replace (dxf_name, 'bak/'+dxf_name+'.bak') '''
    # Обрабатывавшийся файл <name>.dxf превращается в bak/<name>.dxf.bak
    # Если произошла ошибка (невозможно файл переместить в папку bak/),
    #  то он переименовывается в <name>.dxf.bak там, где и был, с заменой

    # As name of otigin file was changed, it recreating
    ## Так как имя исходного файла сменилось, он создаётся заново
    try:
        dxf = open (dxf_name, 'w')    
        dxf.write(new)
        dxf.close()
        # Trying to save to file with exceptions trapping
        ## Попытка записи в файл с перехватом ошибок
    except Exception:
        log = open ('bak/processed.log', 'a')
        log.write('\t'.join('Error',
                            full_name[1], '|',
                            full_name[0], '|',
                            ctime(now()), '\n'
                            ))
        log.close()
        say('Mistake was maked during processing', lang)
        # If was found an exception, it's logging to log
        ## Если возникла ошибка, то сообщение об этом выводится в лог
    else:
        if len(full_name[1]) < 8: t = '\t\t'
        else: t = '\t'
        log = open ('bak/processed.log', 'a')
        log.write(''.join(full_name[1], t,'|\t',
                          full_name[0], '\t|\t',
                          ctime(now()), '\n'
                          ))
        log.close()
        say('All done!', lang)
        # If wasn't found any exceptions, processe's information logging
        # Если не возникло ошибок, в лог выводится информация об обработке

def call_clearing (command=False):
    if not command:
        say('Clearing aborted', lang)
        return False
    if (type(command) == int or
        (type(command) == str and command.isdigit()
         )):
        if int(command) > 9 or confirm():
            need_clear (int(command))
            return True
        else:
            return False
    if (command == True or
        (type(command) == str and confirm(command)
         )):
        need_clear()
        return True
    return False

def confirm (status=None, recursive=False):
    right = ('д', 'да', 'верно', 'истина', 'истинно',
             'y', 'yes', 'yeah', 'right', 'true')
    wrong = ('н', 'нет', 'неверно', 'ошибка', 'ошибочно',
             'n', 'no', 'not', 'wrong', 'false')
    
    if status == None:
        sure = say('Are you sure? ', lang, 'input')
        if sure in right: return True
        elif sure in wrong: return False
        else: return confirm('FaultStr', recursive)
    if type(status) == bool:
        return status
    if type(status) in (int, float):
        if status == 0: return False
        elif status != 1 and recursive:
            return confirm('FaultInt', recursive)
        else: return True
    if type(status) == str:
        if status == 'FaultStr':
            say("Can't understand", lang)
            if recursive:
                say('Try again', lang)
                return confirm (None, recursive)
            return None
        if status == 'FaultInt':
            say('Wrong Int entered', lang)
            new = say('Input 0 or 1: ', lang, 'input')
            if not new.isdigit():
                return confirm ('FaultInt', recursive)
            else: return confirm (int(new), recursive)
        if status in right: return True
        elif status in wrong: return False
        else: return confirm('FaultStr', recursive)

# -- It need to be remaked --
def need_clear (days=45):
    try:
        count = clearing.bak(days)
        ''' print ('Произведена чистка файлов старше', need_clear, 'дней.') '''
        say(('All files older than _ days was deleted.', need_clear), lang)
        if (count%10 == 1 and
            count%100 != 11):
            few_files = 'файл.'
        elif (сount%10 in (2, 3, 4) and
            not count%100 in (12, 13, 14)):
            few_files = 'файла.'
        else: few_files = 'файлов.'
        print (say('Deleted', lang, 'noprint'), count, few_files)
    except Exception:
        return False
    else: return True
# -- It need to be remaked --

__author__ = 'Maksim "DamTerrion" Solovev'

if __name__ == '__main__':
    need = say('Activate clearing? (Yes/Not/Days)', lang, 'input')
    call_clearing(need)
    # Garbage cleaning from user's choice
    #  if this script is main script
    ## Подчистка мусора на выбор пользователя,
    ##  если этот скрипт запущен как основной,
    ##  а не импортирован из другого скрипта.
 
while __name__ == '__main__':
    # Loop working until this is a main script
    ## Цикл выполняется, пока это главный скрипт,
    ##  а не импортированный
    code = say('Input name of DXF-file for processing: ', lang, 'input')
    if code in ('quit', 'exit', 'выход', 'конец') : break
    try: ndxf (code)
    except Exception: say('Mistake was maked', lang)
    # I havn't any idea, how script can be stop being main in loop
    ## Строго говоря, не представляю, как скрипт может
    ##  внутри цикла перестать быть главным
