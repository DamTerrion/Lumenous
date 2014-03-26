from os import path
from os import walk
from os import remove
from time import time as now
from time import ctime

def remove_old_bak (days=60, direction='bak'):
    log = open (direction+'/deleted.log', 'a')
    date = now() - days * 24 * 60 * 60
    log.write(ctime(now())+',\t'+days+'\n'+
              '------------------------\n')
    for name, dirs, files in walk(direction):
        for file in files:
            last = path.getatime(direction+'/'+file)
            if last < date and file[:-4]='.bak' :
                try:
                    remove(direction+'/'+file)
                except Exception:
                    log.write('\t'+"wasn't removed:\n'+
                              '\t'+file+'\t'+ctime(last)+'\n')
                else:
                    log.write('\t'+file+'\t'+ctime(last)+'\n')
    log.write('\n')
    log.close()
