from os import path, walk, remove
from time import ctime, time as now
from confirm import confirm
from local import say, ask

lang = 'RU'

def bak (days=60, direction='bak'):
    if int(days) < 10:
        solution = ask('Limitation less than 10 days, are you confirm?', lang)
        if not confirm(solution):
            return False
    
    date = now() - days * 24 * 60 * 60
    log = open (direction+'/deleted.log', 'a')
    log.write(
        ''.join((ctime(now()), ',\t', str(days), '\n',
                 '------------------------\n'))
              )
    count = 0
    for name, dirs, files in walk(direction):
        for file in files:
            last = path.getatime(direction+'/'+file)
            if (last < date and file[-4:]=='.bak'):
                tt = '\t' * (5 - len(file)//4)
                try:
                    remove(direction+'/'+file)
                except Exception:
                    log.write(
                        ''.join((
                            '\t', "wasn't removed:\n", '\t',
                            file, tt, ctime(last), '\n'
                            ))
                              )
                else:
                    log.write(
                        ''.join(('\t', file, '\t', ctime(last), '\n'))
                              )
                    count += 1
    log.write(
        ''.join(('------------------------\t', str(count), '\n'))
              )
    log.close()
    return count

def call (command=False):
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
        say('Clearing activated', lang)
        need_clear()
        return True
    return False

def need_clear (days=45):
    count = bak(days)
    # say('Few files was deleted.', lang)
    ######
    if (count%10 == 1 and
        count%100 != 11):
        few_files = 'файл.'
    elif (count%10 in (2, 3, 4) and
        not count%100 in (12, 13, 14)):
        few_files = 'файла.'
    else: few_files = 'файлов.'
    ######
    print (say('Deleted', lang, 'noprint'), count, few_files)

if __name__ == '__main__':
    days = ask('Input maximum limitation of files:', lang)
    bak(days)
