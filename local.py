dictionary = dict.fromkeys(['en', 'ru'], {})
dictionary['en'] = {
    'ErrorSent': 'Mistake was making during localization'
    }
dictionary['ru'] = {
    'ErrorSent':
        'Произошла ошибка локализации',
    'File not found':
        'Файл не найден',
    "Can't replace this file to '/bak'!":
        "Невозможно записать этот файл в '/bak'!",
    'Mistake was maked during processing':
        'Произошла ошибка во время обработки',
    'All done!':
        'Всё отлично!',
    'Clearing aborted':
        'Чистка отменена',
    'Are you sure? ':
        'Вы уверены? ',
    "Can't understand":
        'Ответ не ясен',
    'Try again':
        'Попробуйте ещё раз',
    'Wrong Int detected.':
        'Введено неправильное число',
    'Input 0 or 1: ':
        'Введите 0 или 1: ',
    'All files older than _ days was deleted.':
        'Все файлы старше _ дней были удалены.',
    'Deleted':
        'Удалено',
    'Activate clearing? (Yes/Not/Days) ':
        'Произвести чистку? (Да/Нет/Срок) ',
    'Input name of DXF-file for processing: ':
        'Введите имя DXF-файла для обработки: ',
    'Mistake was making':
        'Произошла ошибка'
    }

def phrase (sentence, language='en', action='print'):
    if type(language) == str:
        language = language.lower()
    if not language in dictionary:
        return do (sentence, action)
    if type(sentence) == str:
        if sentence in dictionary[language]:
            return do (dictionary[language][sentence], action)
        else: return do (dictionary[language]['ErrorSent'], action)
    elif type(sentence) == tuple:
        processed = phrase(sentence[0], language, 'noprint')
        return do (processed, action)

def do (sentence, action=False):
    if action == 'print':
        return print (sentence)
    if action == 'input':
        return input (sentence)
    if action == 'noprint':
        return sentence
    return False
