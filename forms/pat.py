from time import ctime, time as now

def load (filename):
    file = open(filename, 'r')
    data, errors = list(), list()
    obj = {'x': 0, 'y': 0,
           'h': 0, 'w': 0,
           'a': 0}
    num = 0
    for line in file:
        num += 1
        key = ''
        value = ''
        for char in line:
            if char.isalpha():
                if key:
                    obj[key] = int(value)
                if char.lower in obj:
                    key = char
                    value = ''
                else:
                    errors.append('Wrong key in line '+str(num)+': '+char)
            elif char.isdigit():
                value += char
            elif char == ';':
                data.append(obj)
                break
            else:
                errors.append('Wrong line N'+str(num))
                break
    file.close()
    if errors:
        error_log = open(filename+'.error', 'a')
        try:
            error_log.write(ctime(now()))
            error_log.write('\n')
            error_log.write('\n'.join(errors))
            error_log.write('\n')
        finally: error_log.close()    
    return data

def print_pat (data):
    for entry in data:
        print(entry)

if __name__ == '__main__':
    file_name = input('Input file name: ')
    data_pat = load(file_name)
    print_pat(data_pat)
