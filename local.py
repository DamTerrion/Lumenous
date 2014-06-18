dictionary = dict.fromkeys(['en', 'ru'], {})
dictionary['en'] = {
    }
dictionary['ru'] = {
    }

def phrase (sentence, language='en'):
    if type(language) == str:
        language = language.lower()
    if not language in dictionary:
        return phrase(sentence)
    if sentence in dictionary[language]:
        return dictionary[language][sentence]
    else: return dictionary[language]['ErrorSent']
