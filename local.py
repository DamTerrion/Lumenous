import json

dictionary = dict.fromkeys(['en', 'ru'], {})

dictionary['en'] = {
    '_ErrorSent_':
        'Localization error happened',
    'Activate clearing? (Yes/Not/Days)':
        None,
    'All done in':
        None,
    'Are you confirm?':
        None,
    'Are you sure?':
        None,
    "Can't replace this file to '/bak'!":
        None,
    "Can't understand":
        None,
    'Clearing aborted':
        None,
    'Clearing activated':
        None,
    'Deleted':
        None,
    'Done!':
        None,
    'Few files was deleted.':
        None,
    'File':
        None,
    'File not found':
        None,
    'Input 0 or 1:':
        None,
    'Input a file name':
        None,
    'Input maximum limitation of files:':
        None,
    'Input name of DXF-file for processing:':
        None,
    'Input name of object for selection:':
        None,
    'Input name of result file:':
        None,
    'Insertion!':
        None,
    'kB':
        None,
    'Limitation less than 10 days, are you confirm?':
        None,
    'Mistake was made':
        None,
    'Mistake was made during processing':
        None,
    'Round base set at':
        None,
    's.':
        None,
    'Try again':
        None,
    'Unknown problem with configuration file.':
        None,
    'Wrong Int entered':
        None
    }

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

    'Deleted1':
        'Удалён',
    
    'Done!':
	'Готово!',
    
    'Few files was deleted.':
        'Несколько файлов были удалены.',
    
    'File1':
        'файл.',
    
    'File2':
        'файла.',
    
    'File5':
        'файлов.',
    
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
    
    'Insertion!':
        'Обнаружен объект-вставка!',
    
    'Limitation less than 10 days, are you confirm?':
        'Срок давности меньше 10 дней, подтверждаете?',
    
    'Mistake was made':
        'Произошла ошибка',
    
    'Mistake was made during processing':
        'Произошла ошибка во время обработки',
    
    'Round base set at':
        'Порядок округления установлен на',
    
    'Try again':
        'Попробуйте ещё раз',
    
    'Unknown problem with configuration file':
        'Неизвестная проблема с конфигурационным файлом',
    
    'Wrong Int entered':
        'Введено неправильное число',
    }


__author__ = {
    'name': "Maksim Solov'ev",
    'nick': 'DamTerrion',
    'email': 'damterrion@yandex.ru'
    }

def check (sentence, language):
    if not isinstance(sentence, str):
        return False
    if not isinstance(language, str):
        return 'en'
    return language.lower()

def think (sentence, language='en'):
    language = check(sentence, language)
    if not language in dictionary:
        language = 'en'
    if sentence in dictionary[language]:
        return dictionary[language][sentence]
    elif (sentence in dictionary['en'] and
          dictionary['en'][sentence]):
        return dictionary['en'][sentence]
    else:
        return sentence

def say (sentence, language='en'):
    print(
        think(sentence, language)
        )
    return True

def ask (sentence, language='en'):
    question_description = ''.join(
        (think(sentence, language), ' ')
        )
    return input(question_description)
