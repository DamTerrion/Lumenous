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
        new = pat.sort(readed)
        splited = file.split('.')
        result = open('.'.join((splited[0],'OPT')), 'w')
        result.write(pat.build(new))
        result.close()
