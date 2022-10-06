from .base_menu import Menu


class LowerLevelMenu(Menu):
    """serves the home menu"""
    def citizen_registration(self):  # 1
        menu_text = "Enter your ID Number(Omang)?\n"
        
        self.session['level'] = 50
        return self.ussd_proceed(menu_text)

    def noncitizen_registration(self):  # 2
        menu_text = "This service is not available yet\n"
        #self.session['level'] = 40
        return self.ussd_end(menu_text)

    def login(self):  # 3
        menu_text = "This service is not available yet\n"
        #self.session['level'] = 40
        return self.ussd_end(menu_text)



    def execute(self):
        menus = {
            '1': self.citizen_registration,
            '2': self.noncitizen_registration,
            '3': self.login
        }
        return menus.get(self.user_response, self.home)()