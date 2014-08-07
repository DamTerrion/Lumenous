dictionary = dict.fromkeys(['en', 'ru'], {})
dictionary['en'] = {
    '_ErrorSent_': 'Mistake was maked during localization'
    }

dictionary['ru'] = {
    '_ErrorSent_':
        'Произошла ошибка локализации',
    
    'Activate clearing? (Yes/Not/Days) ':
        'Произвести чистку? (Да/Нет/Срок) ',
    
    'All done!':
        'Всё готово!',
    
    'All files older than _ days was deleted.':
        'Все файлы старше _ дней были удалены.',
    
    'Are you confirm? ':
        'Подтверждаете? ',
    
    'Are you sure? ':
        'Вы уверены? ',

    "Can't replace this file to '/bak'!":
        "Невозможно записать этот файл в '/bak'!",
    
    "Can't understand":
        'Ответ не ясен',
    
    'Clearing aborted':
        'Чистка отменена',
    
    'Deleted':
        'Удалено',
    
    'Done!':
	'Готово!',
    
    'File not found':
        'Файл не найден',
    
    'Input 0 or 1: ':
        'Введите 0 или 1: ',
    
    'Input a file name ':
        'Введите имя файла: ',
    
    'Input name of DXF-file for processing: ':
        'Введите имя DXF-файла для обработки: ',
    
    'Input name of object for selection: ':
        'Введите имя объекта для выборки: ',
    
    'Input name of result file: ':
        'Введите имя файла для результата: ',
    
    'Mistake was maked':
        'Произошла ошибка',
    
    'Mistake was maked during processing':
        'Произошла ошибка во время обработки',
    
    'Try again':
        'Попробуйте ещё раз',
    
    'Wrong Int entered':
        'Введено неправильное число',
    }

def say (sentence, language='en', action='print'):
    if isinstance(language, str):
        language = language.lower()
    if not language in dictionary:
        return _do(sentence, action)
    if isinstance(language, str):
        if sentence in dictionary[language]:
            return _do(dictionary[language][sentence], action)
        else: return _do(dictionary[language]['_ErrorSent_'], action)
    elif isinstance(sentence, tuple):
        processed = say(sentence[0], language, 'noprint')
        return _do(processed, action)

def _do (sentence, action=False):
    if action == 'print':
        return print(sentence)
    if action == 'input':
        return input(sentence)
    if action == 'noprint':
        return sentence
    return False
