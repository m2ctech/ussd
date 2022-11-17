from .base_menu import Menu






class DashboardMenu(Menu):


    def get_1Gov_ID(self):

        #self.session["level"] = 11

        menu_text = "Enter your 1Gov ID:"

        return self.ussd_proceed(menu_text)

    def get_user_password(self):
        #self.session["level"] = 12

        self.session["id"] = self.user_response

        menu_text = "Enter your password:"

        return self.ussd_proceed(menu_text)


    def authenticate(self):
        #self.session["level"] = 13
        id = self.session.get("id")

        #get password--api call 
        stored_password = "default"

        if self.user_response == stored_password:

            menu_text = ""

            return

        else:
            menu_text = "Invalid Credentials"
            return self.ussd_end(menu_text)


    def view_application(self):
        #self.session["level"] = 14

        #get
        pass



    def __str__(self):
        return "Dashboard"
            
            

        


