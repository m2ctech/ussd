import json
from django.http import HttpResponse
import requests

from django.core.cache import cache



class Menu(object):
    def __init__(self, session_id, session,user_response, phone_number=None, level=None):
        self.session = session
        self.session_id = session_id
        self.user_response = user_response
        self.phone_number = phone_number
        self.level = level
        

    def execute(self):
        raise NotImplementedError

    def ussd_proceed(self, menu_text):
        cache.set(self.session_id, self.session)
        menu_text = "CON {}".format(menu_text)
        response = HttpResponse(menu_text, 200)
        response.headers['Content-Type'] = "text/plain"
        return response

    def ussd_end(self, menu_text):
        cache.delete(self.session_id)
        menu_text = "END {}".format(menu_text)
        response = HttpResponse(menu_text, 200)
        response.headers['Content-Type'] = "text/plain"
        return response

    def home(self):
        """serves the home menu"""
        menu_text = "Welcome to 1Gov,\n Choose an option\n"

        #menu_text += " 1. Register\n"
        menu_text += " 1. Citizen Registration\n"
        menu_text += " 2. Non-Citizen Registration\n"
        menu_text += " 3. Login\n"
        
        self.session['level'] = 1
        
        # print the response on to the page so that our gateway can read it
        return self.ussd_proceed(menu_text)


    def __str__(self):
        return "Base Menu (blueprint)"