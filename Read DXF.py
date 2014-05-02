from math import atan2, degrees
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

def read (dxf_name=False):
    if not dxf_name:
        dxf_name = input ('Введите имя файла: ')
    
    if dxf_name[-4:] != '.dxf' :
        dxf_name += '.dxf'
    
    try:
        dxf_file = open (dxf_name, 'r')
    except FileNotFoundError:
        print ('Файл не найден.')
        return False
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
        print (i, even, i%2)
        if even != i%2:
            couple = get_couple(data, i)
            print (couple)
            if couple: stack.append(couple)
            else: even = not even
    print (stack)
    return stack

def get_couple (data, i):
    marker = data[i].strip()
    print (marker)
    if marker.isdigit():
        marker = int(marker)
        value = data[i+1].strip()
        return (marker, value)
    else: return False

def print_stack():
    stack = read()
    if stack: print (stack)
