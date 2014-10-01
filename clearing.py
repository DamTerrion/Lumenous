from os import path, walk, remove
from time import ctime, time as now
from confirm import confirm

def bak (days=60, direction='bak'):
    if int(days) < 10:
        confirm = ask('Срок давности меньше 10 дней, подтверждаете?', lang)
        if not any (confirm.lower() in var for var in
                    ('yes', 'yeah', 'да', 'верно')):
            return False
    
    date = now() - days * 24 * 60 * 60
    log = open (direction+'/deleted.log', 'a')
    log.write(ctime(now())+',\t'+str(days)+'\n'+
                  '------------------------\n')
    count = 0
    for name, dirs, files in walk(direction):
        for file in files:
            last = path.getatime(direction+'/'+file)
            if (last < date and file[-4:]=='.bak'):
                try:
                    remove(direction+'/'+file)
                except Exception:
                    log.write('\t'+"wasn't removed:\n"+
                                  '\t'+file+'\t'+ctime(last)+'\n')
                else:
                    log.write('\t'+file+'\t'+ctime(last)+'\n')
                    count += 1
    log.write('\n')
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
        need_clear()
        return True
    return False

def need_clear (days=45):
    try:
        count = clearing.bak(days)
        say('Few files was deleted.', lang)
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

if __name__ == '__main__':
    days = ask('Введите максимальную давность файлов:', lang)
    bak(days)
