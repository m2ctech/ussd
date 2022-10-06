

def verify_id(user_id):
    """Validate ID/Omang number """
    if len(user_id) != 9 :
        return False
      
    elif user_id.isnumeric(): 
        return True

    else:
        return False
    
    

def verify_username(text):

    if text.isalpha():
        return True
    else:
        return False

def check_pin(user_pin):

    if len(user_pin) == 4 and user_pin.isnumeric() :
        return True
    else:
        return False

def verify_pin():
    pass
