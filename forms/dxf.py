class primitive (object):
    def __init__ (self, params=dict()):
        self.params = params
        if 0 in params:
            self.name(params[0])
    
    def determ (self, param, value):
        # Добавление или переопределение параметра
        self.params[param] = value
        if param == 0: self.name = value
        return True
    
    def add (self, param, value):
        # Добавление одного или нескольких параметров
        if not param in self.params:
            self.params[param] = value
        elif not isinstance(self.params[param], list):
            old_value = self.params[param]
            self.params[param] = list(old_value)
            self.params[param].extend(param)
        else: self.params[param].extend(param)

def read (file):    
    def valid (param, value):
        # Определение, является ли пара ключ-значение верной
        if isinstance(param, str) and param.isdigit():
            param = int(param)
        elif isinstance(param, int): pass
        else: return False
        
        if isinstance(value, str):
            if param in range(0, 10): pass
            elif param in range(10, 60):
                try: value = float(value)
                except ValueError: return False
            elif param in range(60, 71):
                try: value = int(value)
                except ValueError: return False
        return (param, value)
    
    loaded, stat, last = [], False, ''
    for line in file:
        couple = valid(last.strip(), line.strip())
        if stat and valid:
            loaded.append(couple)
            stat = False
        else: stat = True
        last = line
    return loaded

def openit (name_i=None, name_o=None):
    while not name_i:
        name_i = input('Input name: ')
    file_i = open(name_i, 'r')
    data = read(file_i)
    file_i.close()
    while not name_o:
        name_o = input('Output name: ')
    file_o = open(name_o, 'w')
    for entry in data:
        file_o.write(str(entry)+'\n')
    file_o.close()
    print('done!')

while __name__ == '__main__':
    openit(name_o='output.txt')
