def compare (name1 = False, name2 = False):
    if not name1: name1 = input('File 1: ')
    if not name2: name2 = input('File 2: ')
    
    try:
        file1 = open(name1, 'rb')
        file2 = open(name2, 'rb')
        file3 = open(name1+'+'+name2, 'wb')
    except FileNotFoundError:
        return 'Один из файлов не найден'
    except Exception:
        return 'Неизвестная ошибка'
    else:
        str1 = file1.read()
        str2 = file2.read()

        convergence = [b'', 0]
        discrepancy = 0
        if len(str1) < len(str2):
            L = len(str1)
        else:
            L = len(str2)
        
        for i in range(L):
            if str1[i] == str2[i]:
                convergence[0] += b' '
                convergence[1] += 1
            else:
                convergence[0] += b'#'
                discrepancy += 1
        file3.write(convergence[0])
        return discrepancy
    finally:
        file1.close()
        file2.close()
        file3.close()

if __name__ == '__main__':
    print( compare() )
    
