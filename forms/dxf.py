class Primitive (object):
    def __init__ (self, params=dict()):
        self.params = params
        if isinstance(params, tuple) and len(params) == 2:
            params = dict([params])
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

class Compound (list):
    def __init__ (self, kind=None, name=None, level=0):
        self.setkind(kind)
        self.setname(name)
        self.level = level
    def setkind (self, kind):
        self.kind = kind
    def setname (self, name):
        self.name = name
    def __str__ (self):
        tab = ' '*2
        result = [tab*self.level]
        level = self.level+1
        if self.kind:
            result.append(self.kind)
            if self.name:
                result.append(', ')
        if self.name:
            result.append(self.name)
        result.append(':\n')
        for entry in self:
            if isinstance(entry, tuple):
                result.append(tab*level)
                result.append(repr(entry[0]))
                result.append(': ')
                result.append(repr(entry[1]))
                result.append('\n')
            elif isinstance(entry, Compound):
                result.append(str(entry))
        return ''.join(result)
    
def read (file):    
    def valid (param, value):
        # Определение, является ли пара ключ-значение верной
        if isinstance(param, str) and param.isdigit():
            param = int(param)
        elif isinstance(param, int): pass
        else: return False
        
        if isinstance(value, str):
            if param in range(0, 10):
                try: value = str(value)
                except ValueError: return False
            elif param in range(10, 60):
                try: value = float(value)
                except ValueError: return False
            elif param in range(60, 71):
                try: value = int(value)
                except ValueError: return False
        return (param, value)
    
    loaded = []
    stat = False
    last = ''
    for line in file:
        couple = valid(last.strip(), line.strip())
        if stat and valid:
            loaded.append(couple)
            stat = False
        else: stat = True
        last = line
    return loaded

def construct (data, i=0, until=None, box=True, level=0):
    hard_end = (0, 'EOF')
    break_conditions = {
        (0, 'SECTION'): (0, 'ENDSEC'),
        (0, 'BLOCK'):   (0, 'ENDBLK'),
        (66, 1):        (0, 'SEQEND')
        }
    if not level:
        steps = 1
        result = Compound('file')
    else: steps = 0
    while i < len(data):
        adding = data[i]
        if data[i][0] == 0:
            if not steps:
                result = Compound(kind=data[i][1], level=level)
            else:
                if data[i] == hard_end:
                    break
                if box:
                    if data[i] == until:
                        box = False
                    adding, i = construct(data, i, until, False, level+1)
                else:
                    return result, i
        if data[i] in break_conditions:
            box = True
            until = break_conditions[data[i]]
        if data[i][0] == 2:
            result.name = data[i][1]
        result.append(adding)
        steps += 1
        i += 1
    return result, i

######################################
def resave (name_i=None, name_o=None):
    while not name_i:
        name_i = input('Input name: ')
    file_i = open(name_i, 'r')
    data = read(file_i)
    ready, num = construct(data)
    file_i.close()
    while not name_o:
        name_o = input('Output name: ')
    file_o = open(name_o, 'w')
    '''
    for entry in data:
        file_o.write(
            '{code:>3}, {value!r}\n'.format(
                code=entry[0],
                value=entry[1]
                )
            )
    '''
    try:
        for item in ready:
            file_o.write(str(item))
    except TypeError:
        print ('None!')
    file_o.close()
    print('done!')
    ##############

if __name__ == '__main__':
    resave(name_i='hat.txt', name_o='output.txt')
