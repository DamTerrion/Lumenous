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
    data = dxf_file.read()
    data_stack = []
    even = True
    for i in range(0, len(data), 2):
        if even != i%2:
            couple = get_couple(data, i)
            if couple: data_stack.append(couple)
            else: even = not even
    return data_stack

def get_couple (data, i):
    marker = data[i].strip()
    if marker.isdigit():
        marker = int(marker)
        value = data[i+1].strip()
        return (marker, value)
    else: return False

def print_stack():
    stack = read()
    if stack: print (stack)
