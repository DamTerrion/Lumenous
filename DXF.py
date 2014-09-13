from math import atan2, degrees
from os.path import exists
from Exponion import Exponion, Poynting
from local import say

precision = -4
lang = 'ru' # Ignore this string, if you want to use english in program

def clear_object ():
    return {
        'type'  : None,         # Тип объекта (линия, фигура)
        'layer' : '0',          # Слой объекта
        'colour': 'BYLAYER',    # Цвет объекта, если он задан явно
        'points': [],           # Словарь точек со стороковыми именами
        'vertex': 0,            # Счётчик точек полилинии - число
        'width' : None,         # Ширина полилинии
        'closed': None          # Замкнутость полилинии
        }

'''
def _open_ (dxf_name=False):
    if not dxf_name:
        dxf_name = say('Input a file name ', lang, 'input')
    if exists(dxf_name):
        return open(dxf_name, 'r')
    elif exists(dxf_name+'.dxf'):
        print(dxf_name+'.dxf')
        answer = say('Are you confirm? ', lang, 'input')
        if any(answer.lower() in item for item in ('да', 'yes', 'верно')):
            return open(dxf_name+'.dxf', 'r')
    else:
        say('File not found', lang)
        return False

def _read_ (dxf_name=False):
    dxf_file = _open_(dxf_name)
    while not dxf_file:
        dxf_file = _open_(False)
    data = get_data(dxf_file)
    dxf_file.close()
    return data
'''

# Нужно отладить функцию загрузки файла
# Хорошо бы добавить функцию выгрузки файла
def load (dxf_name):
    try:
        dxf_file = open(dxf_name, 'r')
        data = get_data(dxf_file)
    except OSError:
        say('Ошибка открытия файла', lang)
    except Exception:
        say('Неизвестная ошибка при открытии', lang)
    finally:
        dxf_file.close()
    return data

# Нужно разобраться с функцией получения пары
def get_couple (data, i):
    def _marker_ (marker):
        try:
            assert len(marker) == 4
            assert marker.strip().isdigit()
        except AssertionError: return False
        else: return True
    
    def _value_ (marker, value):
        marker = int(marker.strip())
        try:
            if   marker in range (0, 10):  value =   str(value.strip())
            elif marker in range (10, 60): value = float(value.strip())
            elif marker in range (60, 80): value =   int(value.strip())
            else value = value.strip()
        except ValueError: return False
        else: return value
    
    def _couple_ (A, B):
        marker = int(A.strip())
        value = _value_(A, B)
        return (marker, value)

    A, B = data[i], data[i+1]
    try: C = data[i+2]
    except IndexError: C = '123\n'    
    if _marker_(A):
        if _marker_(C):
            if not _value_(A, B) is False:
                return _couple_(A, B)
            else: return False
        else:
            if not _marker_(B):
                return _couple_(A, B)
            else: return False
    else: return False

# Нужно переименовать 'get_data' в 'extract'
def get_data (dxf_file):
    data = []
    for line in dxf_file:
        data.append(line)
    stack = []
    even = True
    for i in range(0, len(data)-1):
        if even != i%2:
            couple = get_couple(data, i)
            if couple: stack.append(couple)
            else: even = not even
    return stack

# Нужно переименовать 'get_object' в 'elicit'
def get_object (data, name=False):
    stack = []
    if not name:
        name = say('Input name of object for selection: ', lang, 'input')
    for item in data:
        if item[0] == name:
            stack.append(item)
    if len(stack) == 0:
        return False
    if len(stack) == 1:
        return stack[0]
    return stack

######

def structurize (data, name=False, i=0, break_condition=(0, 'EOF')):
    stack = (name, [])
    while i < len(data)-1:
        if (data[i] == break_condition or
            (data[i][0], 'ANY') == break_condition):
            return stack, i
        elif data[i] == (0, 'SECTION'):
            result, i = structurize (data, data[i+1][1], i+2, (0, 'ENDSEC'))
        elif data[i][0] == 0:
            result, i = structurize (data, data[i][1], i+1, (0, 'ANY'))
        else:
            if data[i] == (66, 1):
                break_condition = (0, 'SEQEND')
            result = data[i]
            i += 1
        stack[1].append(result)
    if name: return stack, i+1
    else: return stack[1]

# Нужно убрать функцию 'get', заменив более функциональной
def get (objects, dxf_name=False):
    data = _read_(dxf_name)
    data = structurize(data)
    if objects:
        data = get_object(data, objects)
    return data

# Нужно проверить функциональность функции 'get_head'
def get_head (data):
    stack = []
    for item in data:
        if type(item) in (tuple, list, dict):
            stack.append(item[0])
        if type(item) in (int, str):
            stack.append(item)
    return stack

# Нужно проверить функциональность функции 'print_stack'
# Вероятно, эта функция должна быть вынесена вовне
def print_stack (stack, spaces=''):
    result = []
    for item in stack:
        if isinstance(item, tuple):
            result.extend(print_stack (item, spaces+'  '))
        elif isinstance(item, list):
            result.extend(print_stack (item, spaces+''))
        else:
            result.append(''.join((spaces, str(item), '\n')))
    return result

# Нужно выяснить, что вообще за чертовщина тут творится!
if __name__ == '__main__':
    data = get('ENTITIES')[1]
    printable = print_stack(data)
    result_name = say('Input name of result file', lang, 'input')
    new_file = open(result_name, 'w')
    new_file.write(''.join(printable))
    new_file.close()
    say('Done!', lang)
