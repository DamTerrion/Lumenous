dictionary = dict.fromkeys(['en', 'ru'], {})
dictionary['en'] = {
    '_ErrorSent_': 'Mistake was maked during localization'
    }

'''
Actualy phrases = [
    '_ErrorSent_',
    'Activate clearing? (Yes/Not/Days)',
    'All done in',
    'Are you confirm?',
    'Are you sure?',
    "Can't replace this file to '/bak'!",
    "Can't understand",
    'Clearing aborted',
    'Clearing activated',
    'Deleted',
    'Done!',
    'Few files was deleted.',
    'File not found',
    'Input 0 or 1:',
    'Input a file name',
    'Input maximum limitation of files:',
    'Input name of DXF-file for processing:',
    'Input name of object for selection:',
    'Input name of result file:',
    'kB.',
    'Limitation less than 10 days, are you confirm?',
    'Mistake was made',
    'Mistake was made during processing',
    's.',
    'Try again',
    'Wrong Int entered'
    ]
'''

dictionary['ru'] = {
    '_ErrorSent_':
        'Произошла ошибка локализации',
    
    'Activate clearing? (Yes/Not/Days)':
        'Произвести чистку? (Да/Нет/Срок)',
    
    'All done in':
        'Выполнено за',
    
    'Are you confirm?':
        'Подтверждаете?',
    
    'Are you sure?':
        'Вы уверены?',

    "Can't replace this file to '/bak'!":
        "Невозможно записать этот файл в '/bak'!",
    
    "Can't understand":
        'Ответ не ясен',
    
    'Clearing aborted':
        'Чистка отменена',
    
    'Clearing activated':
        'Чистка запущена',
    
    'Deleted':
        'Удалено',
    
    'Done!':
	'Готово!',
    
    'Few files was deleted.':
        'Несколько файлов были удалены.',
    
    'File not found':
        'Файл не найден',
    
    'Input 0 or 1:':
        'Введите 0 или 1:',
    
    'Input a file name':
        'Введите имя файла:',
    
    'Input maximum limitation of files:':
        'Введите максимальную давность файлов:',
    
    'Input name of DXF-file for processing:':
        'Введите имя DXF-файла для обработки:',
    
    'Input name of object for selection:':
        'Введите имя объекта для выборки:',
    
    'Input name of result file:':
        'Введите имя файла для результата:',
    
    'kB.':
        'кБ.',
    
    'Limitation less than 10 days, are you confirm?':
        'Срок давности меньше 10 дней, подтверждаете?',
    
    'Mistake was made':
        'Произошла ошибка',
    
    'Mistake was made during processing':
        'Произошла ошибка во время обработки',
    
    's.':
        'с.',
    
    'Try again':
        'Попробуйте ещё раз',
    
    'Wrong Int entered':
        'Введено неправильное число',
    }


__author__ = 'Maksim "DamTerrion" Solov\'ev'


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
