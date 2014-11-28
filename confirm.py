from local import say, ask

lang = 'RU'

def confirm (status=None, recursive=False):
    right = ('д', 'да', 'верно', 'истина', 'истинно',
             'y', 'yes', 'yeah', 'right', 'true')
    wrong = ('н', 'нет', 'неверно', 'ошибка', 'ошибочно',
             'n', 'no', 'not', 'wrong', 'false')
    
    if status == None:
        sure = ask('Are you sure?', lang)
        if sure in right: return True
        elif sure in wrong: return False
        else: return confirm('FaultStr', recursive)
    if type(status) == bool:
        return status
    if type(status) in (int, float):
        if status == 0: return False
        elif status != 1 and recursive:
            return confirm('FaultInt', recursive)
        else: return True
    if type(status) == str:
        if status == 'FaultStr':
            say("Can't understand", lang)
            if recursive:
                say('Try again', lang)
                return confirm (None, recursive)
            return None
        if status == 'FaultInt':
            say('Wrong Int entered', lang)
            new = say('Input 0 or 1:', lang, 'input')
            if not new.isdigit():
                return confirm ('FaultInt', recursive)
            else: return confirm (int(new), recursive)
        if   status.lower() in right: return True
        elif status.lower() in wrong: return False
        else: return confirm('FaultStr', recursive)
