from urllib import request
from .base_menu import Menu
from ..utils import verify_username,verify_id, verify_omang_expiry, validate_password, unique_lastname
from ..send_sms import send_sms
import requests
import json

from appwrite.client import Client, AppwriteException
from appwrite.services.account import Account
from appwrite.services.users import Users
from appwrite.services.databases import Databases
from appwrite.id import ID

validate_omang_details = "https://crm.gov.bw/v1/functions/62fcb3f7a138ce17d8f1/executions"
get_user = "http://crmportal.gov.bw:4000/profile/get"


project = "6228825d967b029b65cb"
key = "3edae4867e4bb64183f83348c3378423cfd31ebeb5e76c0505fc839bf848682f8de6fa434175ead160fe6fe8730bb383b4a468031602755a4fb1818f371da18ad14039de279d2e74558233a3ed7a6aef66ce08394c48af7c23b46017643a33ad4209f1d0de306070c33207072be40e08365247bedc47e23f1235473a6e52075b"

head = {'X-Appwrite-Project': project, 'X-Appwrite-key':key}



client = Client()
account = Account(client)
users = Users(client)
databases = Databases(client, 'default')

(client
  .set_endpoint('https://crmportal.gov.bw/v1/users') # Your API Endpoint
  .set_project('6228825d967b029b65cb') # Your project ID
  .set_key('ebf9fcc6cc0e5723fe3d2f795337ba0398577fdc2c56e28c7144ddce40f5e9850a9df1d45e112a845debc6e0801422451a8b5279d05160bc789c8571a3d4ad6a9f2649a2331d6efbd79d87dcf5148c4cc8a922ded779eaced41c15099824897af40e936cc1d233c3eed4a78c187f60f8bcb5e6364e6be68dab85312560897730') # Your secret API key
)





class RegistrationMenu(Menu):
    """Serves registration callbacks"""

    def get_omang_expiry(self):
        # insert user's phone number
        self.session["level"] = 51

        if verify_id(self.user_response):
            self.session["id"] = self.user_response


            payload = {
                "username": f"{self.user_response}"
            }

            response = requests.post(get_user, headers=head, json=payload)
            r = response.json()
            if r["payload"]:
                menu_text = "Already registered"
                return self.ussd_end(menu_text)
            else:
                menu_text = "Enter your omang expiry date: dd-mm-yyyy"
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

        if verify_omang_expiry(self.user_response):
            self.session["idexp"] = self.user_response

            menu_text = "Enter your first name:"

            return self.ussd_proceed(menu_text)
        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)
        

    def get_lastname(self):
        # insert user's phone number
        self.session["level"] = 53


        if verify_username(self.user_response):
            self.session["fname"] = self.user_response
            menu_text = "Enter your last name:"
            return self.ussd_proceed(menu_text)
        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)


    def get_password(self):
        self.session["level"] = 54

        if verify_username(self.user_response) or unique_lastname(self.user_response):
            self.session["lname"] = self.user_response
            menu_text = "NB: Create a strong password \n Enter your password:"
            return self.ussd_proceed(menu_text)

        else:
            menu_text = "Invalid Input"
            return self.ussd_end(menu_text)


    def get_verify_password(self):
        
        menu_text = validate_password(self.user_response)

        if "must" in menu_text:
            return self.ussd_proceed(menu_text)
        elif "Invalid" in menu_text:
            return self.ussd_end(menu_text)
        else:
            #session
            self.session["level"] = 55
            self.session["password"] = self.user_response
            return self.ussd_proceed(menu_text)

    def create_user_profile(self, first_name, last_name, date_of_birth, gender, marital_status, place_of_birth):

        databases.create_document(database_id="default", collection_id="62b55ee05058149caf6a", document_id="unique()", data={
            "first_name": f"{first_name.isupper()}",
            "middle_name": f"{first_name.isupper()}",
            "surname": f"{last_name.isupper()}",
            "avatar": f"https://ui-avatars.com/api/?name={first_name.isupper()}+{last_name.isupper()}&background=fff&color=69c5ec&rounded=true&bold=true&size=128",
            "date_of_birth": f"{date_of_birth}",
            "gender": f"{gender}",
            "marital_status": f"{marital_status}",
            "employment_status": "-- Select option --",
            "education_level": "-- Select option --",
            "country_of_birth": "Botswana",
            "nationality": "Botswana",
            "primary_phone": f"{{\"is_primary\":true,\"platforms\":\"sms\",\"number\":\"{self.phone_number}\",\"verified\":true}}",
            "primary_email": "{\"is_primary\":false,\"email\":\"null\",\"verified\":false}",
            "citizenship": "Citizen",
            "preferred_comms_channel": "SMS",
            "place_of_birth": f"{place_of_birth}",
            "passport_number": [],
            "passport_photo": None,
            "other_contacts": None,
            "primary_physical": "{}",
            "primary_postal": "{}",

        },
        read=['role:all'],
        write=['role:all']
        )

    def send_message(self):
        # insert user's phone number
        user_password = self.session.get("password")


        if self.user_response == user_password:
            id = self.session.get("id")
            id_exp = self.session.get("idexp")
            first_name = self.session.get("fname")
            first_name = first_name.capitalize()
            lastname = self.session.get("lname")

            payload = {
                "async": False,
                "data": f"{{\"user_id\":\"{id}\",\"expiry_date\":\"{id_exp}\",\"surname\":\"{lastname}\",\"firstname\":\"{first_name}\"}}"
            }

            response = requests.post(validate_omang_details, headers=head, json=payload)
            
            r = response.json()

            data = r["response"]
            response = json.loads(data)


            if response["message"]:
                #CREATE PROFILE CODE GOES HERE
                profile_payload = response["payload"]
                profile_data = json.loads(profile_payload)
                
                #Extract data
                date_of_birth = profile_data["BIRTH_DTE"]
                gender_data = profile_data["SEX"]
                gender = "Male" if gender_data == "M" else "Female"
                marital_status = profile_data["MARITAL_STATUS_DESCR"]
                place_of_birth = profile_data["BIRTH_PLACE_NME"]

                try:
                    result = users.create(f'{id}', f'{id}@1gov.bw', None, f'{user_password}', f'{first_name}')
                    second_result = self.create_user_profile(first_name,lastname, date_of_birth, gender, marital_status, place_of_birth)
                    print(result)
                    print(second_result)
                    menu_text = "You have successfully registered, thank you"
                    send_sms().sending(self.phone_number,first_name,id)
                    return self.ussd_end(menu_text)
                except AppwriteException as e:
                    print(e.message)
                    menu_text = e.message
                    return self.ussd_end(menu_text)
                    

                
            else:
                menu_text = "Invalid Credentials"
                return self.ussd_end(menu_text)


        else:
            menu_text = "Passwords do not Match"
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
            return self.get_password()

        if self.session["level"] == 54:
            return self.get_verify_password()

        if self.session["level"] == 55:
            return self.send_message()


        else:
            return self.get_username()