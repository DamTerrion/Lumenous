from os import path, mkdir, walk, remove
from time import ctime, time as now
from confirm import confirm
from local import say, ask, think

lang = 'RU'

def bak (days=60, direction='bak'):
    if int(days) < 10:
        solution = ask('Limitation less than 10 days, are you confirm?', lang)
        if not confirm(solution):
            return False
    
    date = now() - days * 24 * 60 * 60
    try:
        log = open (direction+'/deleted.log', 'a')
    except FileNotFoundError:
        if not path.exists('bak'):
            mkdir ('bak')
        log = open (direction+'/deleted.log', 'w')
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
                        ''.join(('\t', file, tt, ctime(last), '\n'))
                              )
                    count += 1
    log.write(
        ''.join(('------------------------\t', str(count), '\n\n'))
              )
    log.close()
    return count

def call (command=False):
    if not command:
        say('Clearing aborted', lang)
        return False
    if (isinstance(command, int) or
        (isinstance(command, str) and command.isdigit()
         )):
        if int(command) > 9 or confirm():
            need_clear (int(command))
            return True
        else:
            return False
    if (command is True or
        (isinstance(command, str) and confirm(command)
         )):
        say('Clearing activated', lang)
        need_clear()
        return True
    return False

def need_clear (days=45):
    count = bak(days)
    if (count%10 == 1 and
        count%100 != 11):
        deleted = think('Deleted1', lang)
        few_files = think('File1', lang)
    elif (count%10 in (2, 3, 4) and
        not count%100 in (12, 13, 14)):
        deleted = think('Deleted', lang)
        few_files = think('File2', lang)
    else:
        deleted = think('Deleted', lang)
        few_files = think('File5', lang)
    print (deleted, count, few_files)

if __name__ == '__main__':
    days = ask('Input maximum limitation of files:', lang)
    bak(days)
