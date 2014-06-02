dictionary = dict.fromkeys(['en', 'ru'], {})
dictionary['en'] = {
    'FileName'  : 'Input a file name: ',
    'Confirm'   : 'Are you confirm ',
    'NotFound'  : 'File not found.',
    'ObjectName': 'Input name of object for selection: ',
    'ResultFile': 'Input name of result file: ',
    'Done'      : 'Done!',
    'ErrorSent' : '--Error Sentence!--'
    }
dictionary['ru'] = {
    'FileName'  : 'Введите имя файла: ',
    'Confirm'   : 'Подтверждаете ',
    'NotFound'  : 'Файл не обнаружен',
    'ObjectName': 'Введите имя объекта для выборки: ',
    'ResultFile': 'Введите имя файла для результата: ',
    'Done'      : 'Готово!'
    'ErrorSent' : '--Ошибка фразы!--'
    }

def phrase (sentence, language='en'):
    if type(language) == str:
        language = language.lower()
    if not language in dictionary:
        return phrase(sentence)
    if sentence in dictionary[language]:
        return dictionary[language][sentence]
    else: return dictionary[language]['ErrorSent']
