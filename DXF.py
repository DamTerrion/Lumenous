from math import atan2, degrees
from os.path import exists
from SimplyLine import *

precision = -4

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

def open_file (dxf_name=False):
    if not dxf_name:
        dxf_name = input ('Введите имя файла: ')
    if exists(dxf_name):
        answer = input ('Подтверждается '+dxf_name+'? ')
        if any(answer.lower() in item for item in ('да', 'yes', 'верно')):
            return open (dxf_name, 'r')
        else: return False
    elif exists(dxf_name+'.dxf'):
        answer = input ('Подтверждается '+dxf_name+'.dxf? ')
        if any(answer.lower() in item for item in ('да', 'yes', 'верно')):
            return open (dxf_name+'.dxf', 'r')
    else:
        print ('Файл не обнаружен.')
        return False

def read (dxf_name=False):
    dxf_file = open_file(dxf_name)
    while not dxf_file:
        dxf_file = open_file(False)
    data = get_data(dxf_file)
    dxf_file.close()
    return data

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

def couple (A, B):
    
    marker = int(A.strip())
    value = check_value (A, B)
    return (marker, value)

def check_marker (marker):
    
    try:
        assert len(marker) == 4
        assert marker.strip().isdigit()
    except AssertionError:
        return False
    else: return True

def check_value (marker, value):
    marker = int(marker.strip())
    try:
        if marker in range (0, 10):
            value = str(value.strip())
        elif marker in range (10, 60):
            value = float(value.strip())
        elif marker in range (60, 80):
            value = int(value.strip())
    except ValueError:
        return False
    else: return value

def get_couple (data, i):
  
    A, B = data[i], data[i+1]
    try: C = data[i+2]
    except IndexError: C = '123\n'
    
    if check_marker (A):
        if check_marker (C):
            if not check_value (A, B) is False:
                return couple (A, B)
            else: return False
        else:
            if not check_marker (B):
                return couple (A, B)
            else: return False
    else: return False
    

def data_list (data, name=False, i=0, break_condition=(0, 'EOF')):
    stack = (name, [])
    while i < len(data)-1:
        if ( data[i] == break_condition or
            (data[i][0], 'ANY') == break_condition):
            return stack, i
        elif data[i] == (0, 'SECTION'):
            result, i = data_list (data, data[i+1][1], i+2, (0, 'ENDSEC'))
        elif data[i][0] == 0:
            result, i = data_list (data, data[i][1], i+1, (0, 'ANY'))
        else:
            if data[i] == (66, 1):
                break_condition = (0, 'SEQEND')
            result = data[i]
            i += 1
        stack[1].append(result)
    if name: return stack, i+1
    else: return stack[1]

def print_stack (stack, spaces=''):
    result = []
    for item in stack:
        if type(item) == tuple:
            result.extend(print_stack (item, spaces+'  '))
        elif type(item) == list:
            result.extend(print_stack (item, spaces+''))
        else:
            result.append(spaces+str(item)+'\n')
    return result

def get_object (data, name):
    stack = []
    for item in data:
        if item[0] == name:
            stack.append(item)
    if len(stack) == 0:
        return False
    if len(stack) == 1:
        return stack[0]
    return stack

if __name__ == '__main__':
    readed = read('Stuffs/FQ.dxf')
    data = data_list(readed)
    entities = get_object(data, 'ENTITIES')
    for_print = print_stack(entities)
    new_file = open ('Stuffs/result.txt', 'w')
    new_file.write(''.join(for_print))
    new_file.close()
    print ('Готово!')
