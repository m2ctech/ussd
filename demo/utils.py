
import re

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



def verify_omang_expiry(date):
    check_value = 0
    if "-" in date:
        date_array = date.split("-")
        if len(date_array) == 3:
            if len(date_array[0])==2 and date_array[0].isnumeric():
                check_value += 1

            if len(date_array[1])==2 and date_array[1].isnumeric():
                check_value += 1
    
            if len(date_array[2])==4 and date_array[2].isnumeric():
                check_value += 1
            return True if check_value == 3 else False
        else:
            return False
    else:
        return False


def validate_password(password):

    pattern = re.compile(r'')

    menu_text = ""
    if (len(password)<8):
        menu_text = "NB: Your password must be eight characters long \n Enter your password:"
        
    elif re.search(r'[!@#$%&]', password) is None:
        menu_text = "NB: Your password must contain atleast one special symbol \n Enter your password:"
        
    elif re.search(r'\d', password) is None:
        menu_text = "NB: Your password must contain atleast one digit \n Enter your password:"
    
    elif re.search(r'[A-Z]', password) is None:
        menu_text = "NB: Your password must contain atleast one capital letter \n Enter your password:"
        
    elif re.search(r'[a-z]', password) is None:
        menu_text = "Your password must contain atleast one lowercase letter \n Enter your password:"
        
        
    elif re.match(r'[a-z A-Z 0-9 !@#$%&]{8}', password):
        pattern = re.compile(r'[a-z A-Z 0-9 !@#$%&]{8}')
        result = pattern.match(password)
        menu_text = "Verify your password:"
        
    else:
        menu_text= "Invalid password"

    return menu_text


def unique_lastname(lastname):
    
    if "." in lastname:
        new_array = lastname.split(".")
        for word in new_array:
            result = word.isalpha()
            if not result:
                return False
        return True
    
    
    elif "-"  or " " in lastname:
        new_array = lastname.split("-") if "-" in lastname else lastname.split(" ")
        if len(new_array) == 2 and new_array[0] and new_array[1]:
            result =  True if new_array[0].isalpha() and new_array[1].isalpha() else False
            return result
            
        else:
            result = False
            return result
            
    else:
        return False
