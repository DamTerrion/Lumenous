from os import replace, path, listdir, remove

def check (floppy_path="A:\\",
           disk_path="D:\\YandexDisk\\WORK\\5062N\\ZDN5062\\"):
    floppy_list = listdir(floppy_path)
    disk_list = listdir(disk_path)
    result = list()
    for file_name in floppy_list:
        if file_name in disk_list:
            if compare(disk_path+file_name, floppy_path+file_name):
                print('С', file_name, 'возникла проблема, исправляю.')
                try:
                    remove(floppy_path+file_name)
                    src = open(disk_path+file_name, 'rb')
                    dst = open(floppy_path+file_name, 'wb')
                    for string in src:
                        dst.write(string)
                finally:
                    src.close()
                    dst.close()
                floppy_list.append(file_name)
                result.append(file_name)
            else: print(file_name, '\tпроверен.')
    return result

def compare (name1=None, name2=None):
    if not name1: name1 = input('Файл 1: ')
    if not name2: name2 = input('Файл 2: ')
    file1, file2 = open(name1, 'rb'), open(name2, 'rb')
    str1, str2 = file1.read(), file2.read()
    file1.close()
    file2.close()
    len1, len2 = len(str1), len(str2)
    discrepancy = 0
    if len1 < len2:
        minlen = len1
        discrepancy += len2 - len1
    else:
        minlen = len2
        discrepancy += len1 - len2
    for n in range(minlen):
        if str1[n] != str2[n]:
            discrepancy += 1
    return discrepancy

if __name__ == '__main__':
    result = check()
    for entry in result:
        print(entry)
    print ('\nПроверка закончена')
    answer = input('Нажмите "Enter".')
