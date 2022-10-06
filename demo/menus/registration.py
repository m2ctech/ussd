from urllib import request
from .base_menu import Menu
from ..utils import verify_username,verify_id
from ..send_sms import send_sms
import requests

validate_omang_details = "https://crm.gov.bw/v1/functions/62fcb3f7a138ce17d8f1/executions"

class RegistrationMenu(Menu):
    """Serves registration callbacks"""

    def get_omang_expiry(self):
        # insert user's phone number
        self.session["level"] = 51

        if verify_id(self.user_response):
            self.session["id"] = self.user_response
            menu_text = "Enter your omang expiry date: yyyy-mm-dd"
            return self.ussd_proceed(menu_text)
        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)

        
        

    def get_firstname(self):
        #if username or not User.by_username(username):  # check if user entered an option or username exists
            #self.user = User.create(username=username, phone_number=self.phone_number)
            
            #validate user id first
        #menu_text = verify_id(self.user_response)

        self.session["level"] = 52
        self.session["idexp"] = self.user_response

        menu_text = "Enter your first name"

        return self.ussd_proceed(menu_text)
        

    def get_lastname(self):
        # insert user's phone number
        self.session["level"] = 53


        if verify_username(self.user_response):
            self.session["fname"] = self.user_response
            menu_text = "Enter your last name"
            return self.ussd_proceed(menu_text)
        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)

    def send_message(self):
        # insert user's phone number


        if verify_username(self.user_response):
            self.session["lname"] = self.user_response
            id = self.session.get("id")
            id_exp = self.session.get("idexp")
            first_name = self.session.get("fname")
            lastname = self.session.get("lname")

            payload = {
                "async": False,
                "data": f"{{\"user_id\":\"{id}\",\"expiry_date\":\"{id_exp}\",\"surname\":\"{lastname}\",\"firstname\":\"{first_name}\"}}"
            }

            response = request.post(validate_omang_details, json=payload)
            r = response.json()

            if r.response.success:
                menu_text = "You have successfully registered, thank you"
                send_sms().sending(self.phone_number)
                return self.ussd_end(menu_text)
            else:
                menu_text = "Invalid Credentials"
                return self.ussd_end(menu_text)


        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)
            # go to home
            #return self.home()
        #else:  # Request again for name - level has not changed...
           # menu_text = "Username is already in use. Please enter your username \n"
            #return self.ussd_proceed(menu_text)

    def execute(self):
        if self.session["level"] == 50:
            return self.get_omang_expiry()

        if self.session["level"] == 51:
            return self.get_firstname()

        if self.session["level"] == 52:
            return self.get_lastname()

        if self.session["level"] == 53:
            return self.send_message()


        else:
            return self.get_username()