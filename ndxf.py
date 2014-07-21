from os import replace, path, mkdir
from time import ctime, time as now
import clearing
from local import phrase

lang = 'ru'

def ndxf (dxf_name):
    new = Param = Value = ''
    
    if dxf_name[-4:] != '.dxf' :
        dxf_name += '.dxf'
    print (dxf_name)
    
    try:
        dxf = open (dxf_name, 'r')
        # Файл открывается для считывания
    except FileNotFoundError:
        phrase('File not found', lang)
        return False
    
    Allowed = { '_INIT_':    (' 0', ' 8'),      # Имя и слой каждого объекта
                'POLYLINE':  ('40', '41',       # Начальная и конечная ширина линии
                              '66', '70'),      # Флаг примитивов и замкнутость линии
                'SOLID':     ('10', '20',       # Координаты первой вершины
                              '11', '21',       # Координаты второй вершины
                              '12', '22',       # Координаты третьей вершины
                              '13', '23'),      # Координаты четвёртой вершины
                'VERTEX':    ('10', '20',       # Координаты точки
                              '42'),            # Выпуклость линии
                'LINE':      ('10', '20',       # Координаты начала отрезка
                              '11', '21',),     # Координаты конца  отрезка
                'ARC':       ('10', '20',       # Координаты центра дуги
                              '40', '50', '51'),# Радиус, начальный и конечный углы дуги
                'CIRCLE':    ('10', '20',       # Координаты центра
                              '40'),            # Радиус окружности
                'SEQEND':    ()}                # Объект окончания полилинии
    
    while not (Param == '  2\n' and Value == 'ENTITIES\n'):
        # Если не начался раздел ENTITIES, файл просто просматривается
        Param = dxf.readline()
        Value = dxf.readline()
        
    else :
        # Если же раздел ENTITIES начался, сразу же записывается его заголовок
        new += '  0\n'+'SECTION\n'+'  2\n'+'ENTITIES\n'
        inObject = ''
        
        while not (Param == '  0\n' and Value == 'ENDSEC\n'):
            # Цикл работает до тех пор, пока не закончится раздел
            Param = dxf.readline()
            Value = dxf.readline()
            
            if Param == '  0\n' :       # Если встречается код 0, значит, начался объект,
                inObject = Value[:-1]   #  и требуется определить и сохранить тип объекта

            if (inObject in Allowed and
                (Param[1:-1] in Allowed['_INIT_'] or
                 Param[1:-1] in Allowed[inObject])):
                    # Если рассматривается правильная пара объект-параметр, она записывается
                    new += Param + Value
        else:
            # Раздел кончился, можно расслабиться и завершить запись данных
            new += '  0\n'+'ENDSEC\n'+'  0\n'+'EOF\n'
            
    dxf.close()
    if path.exists('bak') == False :
        mkdir ('bak')
    full_name = path.split(path.abspath(dxf_name))
    try: replace (dxf_name, 'bak/'+full_name[1]+'.bak')
    except Exception:
        replace (dxf_name, dxf_name+'.bak')
        phrase("Can't replace this file to '/bak'!", lang)
    #replace (dxf_name, 'bak/'+dxf_name+'.bak')
    # Обрабатывавшийся файл <name>.dxf превращается в bak/<name>.dxf.bak
    # Если произошла ошибка (невозможно файл переместить в папку bak/),
    #  то он переименовывается в <name>.dxf.bak там, где и был, с заменой

    # Так как имя исходного файла сменилось, он создаётся заново
    try:
        dxf = open (dxf_name, 'w')    
        dxf.write(new)
        dxf.close()
        # Попытка записи в файл с перехватом ошибок
    except Exception:
        log = open ('bak/processed.log', 'a')
        log.write('\t'+
                  'Error!'+'\t'+
                  full_name[1]+'\t|\t'+
                  full_name[0]+'\t|\t'+
                  ctime(now())+'\n')
        log.close()
        prase ('Mistake was maked during processing', lang)
        # Если возникла ошибка, то сообщение об этом выводится в лог
    else:
        if len(full_name[1]) < 8: t = '\t\t'
        else: t = '\t'
        log = open ('bak/processed.log', 'a')
        log.write(full_name[1]+t+'|\t'+
                  full_name[0]+'\t|\t'+
                  ctime(now())+'\n')
        log.close()
        phrase('All done!', lang)
        # Если не возникло ошибок, в лог выводится информация об обработке

def call_clearing (command=False):
    if not command:
        phrase('Clearing aborted', lang)
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
        sure = prase('Are you sure?', lang, 'input')
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
            phrase("Can't understand", lang)
            if recursive:
                phrase('Try again', lang)
                return confirm (None, recursive)
            return None
        if status == 'FaultInt':
            phrase('Wrong Int detected.', lang)
            new = prase('Input 0 or 1: ', lang, 'input')
            if not new.isdigit():
                return confirm ('FaultInt', recursive)
            else: return confirm (int(new), recursive)
        if status in right: return True
        elif status in wrong: return False
        else: return confirm('FaultStr', recursive)

def need_clear (days=45):
    try:
        count = clearing.bak(days)
        #print ('Произведена чистка файлов старше', need_clear, 'дней.')
        phrase(('All files older than _ days was deleted.', need_clear), lang)
        if (count%10 == 1 and
            count%100 != 11):
            few_files = 'файл.'
        elif (сount%10 in (2, 3, 4) and
            not count%100 in (12, 13, 14)):
            few_files = 'файла.'
        else: few_files = 'файлов.'
        print (phrase('Deleted', lang, 'noprint'), count, few_files)
    except Exception:
        return False
    else: return True

__author__ = 'Максим "ДамТеррион" Соловьёв'

if __name__ == '__main__':
    need = phrase('Activate clearing? (Yes/Not/Days)', lang, 'input')
    call_clearing(need)
    # Подчистка мусора на выбор пользователя,
    #  если этот скрипт запущен как основной,
    #  а не импортирован из другого скрипта.
 
while __name__ == '__main__':
    # Цикл выполняется, пока это главный скрипт,
    #  а не импортированный
    code = phrase('Input name of DXF-file for processing', lang, 'input')
    if code in ('quit', 'exit', 'выход', 'конец') : break
    try: ndxf (code)
    except Exception: phrase('Mistake was making', lang)
    # Строго говоря, не представляю, как скрипт может
    #  внутри цикла перестать быть главным
