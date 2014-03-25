from os import path
from os import walk

def remove_old_bak (days, direction):
    for name, dirs, files in walk(direction):
        for file in files:
            if path.getatime('''Путь к файлам''') < '''Текущее время''' - days * 24 * 60 * 60 :
                print (file, 'True')
                # В конечном счёте этот скрипт должен удалять слишком старые файлы
                # Но пока что хотелось бы, чтобы он хотя бы показывал, старые ли они
            else:
                print (file, 'False')

remove_old_bak (10, 'PDF')
