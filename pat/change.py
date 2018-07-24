from os import path
import pat

def multiply (name, value):
    file = open(name)
    inner = pat.read(file)
    file.close()
    for item in inner:
        for key in item:
            if key != 'A':
                item[key] = item[key] * value
    result = pat.build(inner)
    output = open ('r'+name, 'w')
    output.write(result)
    output.close()
    return None
