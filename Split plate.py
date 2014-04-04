def plate (name):
    if type(name) is int: return (None, name, 1)
    
    elif type(name) is str:
        split = name.split('x')
        
        if len(split) == 2: size, mode = split[0], split[1]
        else: mode = '1'
        
        if size[0] in ('A', 'M'): gen, size = size[0], size[1:]
        else: gen = None
        
        if size.isdigit(): size = int(size)
        else: return 'Error: wrong size'
        
        if mode.isdigit() and int(mode) in (1, 4): mode = int(mode)
        else: return 'Error: wrong mode'

        return (gen, size, mode)
    
    else: return 'Error: wrong type'
