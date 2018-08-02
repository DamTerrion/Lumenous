from forms import pat
from os import listdir

for file in listdir():
    if (
        file.lower().endswith('.pat')
        or file.lower().endswith('.opt')
        or file.lower().endswith('.opg')
        ):
        source = open(file)
        readed = pat.parse(source)
        source.close()
        new = pat.mult_all(readed, 4)
        splited = file.split('.')
        splited[0] += '4'
        result = open('.'.join(splited), 'w')
        result.write(pat.build(new))
        result.close()
