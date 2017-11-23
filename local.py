import json

dictionary = dict.fromkeys(['en', 'ru'], {})
dictionary['en'] = {
    '_ErrorSent_': 'Localization error happened'
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
    'File',
    'File not found',
    'Input 0 or 1:',
    'Input a file name',
    'Input maximum limitation of files:',
    'Input name of DXF-file for processing:',
    'Input name of object for selection:',
    'Input name of result file:',
    'Insertion!',
    'kB.',
    'Limitation less than 10 days, are you confirm?',
    'Mistake was made',
    'Mistake was made during processing',
    's.',
    'Try again',
    'Unknown problem with configuration file.',
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
    
    'Unknown problem with configuration file':
        'Неизвестная проблема с конфигурационным файлом',
    
    'Wrong Int entered':
        'Введено неправильное число',
    }


__author__ = 'Maksim "DamTerrion" Solov\'ev'

def check (sentence, language):
    if not isinstance(sentence, str):
        return False
    if not isinstance(language, str):
        return 'en'
    return language.lower()

def think (sentence, language='en'):
    language = check(sentence, language)
    if not language:
        sentence = ' '.join(
            ('|Error: <', sentence, '> Language was not set|')
            )
        return sentence
    if not language in dictionary:
        language = 'en'
    if sentence in dictionary[language]:
        sentence = dictionary[language][sentence]
    elif language != 'en':
        sentence = think(sentence, 'en')
    else:
        sentence = ' '.join(
            ('|Error: <', sentence, '> Sentence was not found in local.py|')
            )
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
