def confirm (status=None, recursive=False):
    right = ('д', 'да', 'верно', 'истина', 'истинно',
             'y', 'yes', 'yeah', 'right', 'true')
    wrong = ('н', 'нет', 'неверно', 'ошибка', 'ошибочно',
             'n', 'no', 'not', 'wrong', 'false')
    
    if status == None:
        sure = ask('Are you sure?', lang)
        if sure in right: return True
        elif sure in wrong: return False
        else: return confirm('_FaultStr_', recursive)
    if type(status) == bool:
        return status
    if type(status) in (int, float):
        if status == 0: return False
        elif status != 1 and recursive:
            return confirm('_FaultInt_', recursive)
        else: return True
    if type(status) == str:
        if status == '_FaultStr_':
            say("Can't understand", lang)
            if recursive:
                say('Try again', lang)
                return confirm (None, recursive)
            return None
        if status == '_FaultInt_':
            say('Wrong Int entered', lang)
            new = say('Input 0 or 1:', lang, 'input')
            if not new.isdigit():
                return confirm ('_FaultInt_', recursive)
            else: return confirm (int(new), recursive)
        if status in right: return True
        elif status in wrong: return False
        else: return confirm('_FaultStr_', recursive)
