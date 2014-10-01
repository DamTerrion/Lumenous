dictionary = dict.fromkeys(['en', 'ru'], {})
dictionary['en'] = {
    '_ErrorSent_': 'Mistake was made during localization'
    }

'''
Actual phrases = [
    '_ErrorSent_',
    '_FaultInt_',
    '_FaultStr_',
    'Activate clearing? (Yes/Not/Days)',
    'All done!',
    'Are you confirm?',
    'Are you sure?',
    "Can't understand",
    "Can't replace this file to '/bak'!",
    'Clearing aborted',
    'Deleted',
    'Done!',
    'Few files was deleted.',
    'File not found',
    'File Opening Error',
    'Input 0 or 1:',
    'Input a file name',
    'Input maximum limitation of files:',
    'Input name of DXF-file for processing:',
    'Input name of object for selection:',
    'Input name of result file:',
    'Limitation less than 10 days, are you confirm?',
    'Mistake was made',
    'Mistake was made during processing',
    'Try again',
    'Wrong Int entered'
    ]
'''

dictionary['ru'] = {
    '_ErrorSent_':
        'Произошла ошибка локализации',
    
    'All done!':
        'Всё готово!',
    
    'Are you confirm?':
        'Подтверждаете?',
    
    'Are you sure?':
        'Вы уверены?',
    
    "Can't understand":
        'Ответ не ясен',
    
    'Deleted':
        'Удалено',
    
    'Done!':
	'Готово!',
    
    'File not found':
        'Файл не найден',
    
    'Input 0 or 1:':
        'Введите 0 или 1:',
    
    'Input a file name':
        'Введите имя файла:',
    
    'Input name of DXF-file for processing:':
        'Введите имя DXF-файла для обработки:',
    
    'Input name of object for selection:':
        'Введите имя объекта для выборки:',
    
    'Input name of result file:':
        'Введите имя файла для результата:',
    
    'Mistake was made':
        'Произошла ошибка',
    
    'Mistake was made during processing':
        'Произошла ошибка во время обработки',
    
    'Try again':
        'Попробуйте ещё раз',
    
    'Wrong Int entered':
        'Введено неправильное число',
    }

def say (sentence, language='en', action='print'):
    if (isinstance(language, str) and isinstance(sentence, str)):
        language = language.lower()
    else: return False
    if action == 'input':
        return ask(sentence, language)
    if not language in dictionary:
        language = 'en'
    if sentence in dictionary[language]:
        sentence = dictionary[language][sentence]
    if action in ['print', 'p']:
        return print(sentence)
    if action in ['noprint', 'np']:
        return sentence

def ask (sentence, language='en'):
    if (isinstance(language, str) and isinstance(sentence, str)):
        language = language.lower()
    else: return False
    if not language in dictionary:
        language = 'en'
    if sentence in dictionary[language]:
        sentence = dictionary[language][sentence]
    return input(sentence+' ')
