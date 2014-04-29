def compareit (name1 = False, name2 = False):
    if not name1: name1 = input ('Name1: ')
    if not name2: name2 = input ('Name2: ')
    
    try:
        file1 = open (name1, 'rb')
        file2 = open (name2, 'rb')
        file3 = open (name1+'+'+name2, 'wb')
    except FileNotFoundError:
        return 'Один из файлов не найден'
    except Exception:
        return 'Неизвестная ошибка'

    str1 = file1.read()
    str2 = file2.read()

    Compare = b''
    if len(str1) < len(str2):
        L = len(str1)
    else:
        L = len(str2)
    
    for i in range(L):
        if str1[i] == str2[i]:
            Compare += b' '
        else:
            Compare += b'#'
    file3.write(Compare)

    file1.close()
    file2.close()
    file3.close()

    return 'Успех'

if __name__ == '__main__': compareit()
