import json


from django.shortcuts import render
from django.core.cache import cache

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests

from .menus.base_menu import Menu
from .menus.home import LowerLevelMenu
from .menus.registration import RegistrationMenu

headers = {"Content-type": "application/json"}
userurl = "http://localhost:3000/users"
urlusers = "https://accdev.gov.bw/v1/functions/62ea0b812a1c3ca93ab9/executions"

@csrf_exempt
def index(request):

  """Handles post call back from AT"""

  if request.method == 'POST':
    session_id = request.POST.get('sessionId')
    service_code = request.POST.get('serviceCode')
    phone_number = request.POST.get('phoneNumber')
    text = request.POST.get('text')

    response = requests.get(urlusers)
    users = response.json()
    print(users) 

    
    text_array = text.split("*")
    #reversed_text_array = text_array.reverse()
    text_array.reverse()
    user_response = text_array[0]

    if cache.get(session_id):
      session = cache.get(session_id)
    else:
      session = {"level":0, "session_id":session_id, "id": "default", "idexp": "default", "fname":"default", "lname":"default"}
      cache.set(session_id, session)

    level = session.get("level")

    if level < 2:
        menu = LowerLevelMenu(session_id=session_id, session=session, phone_number=phone_number,
                              user_response=user_response)
        return menu.execute()
      
    if level >= 50:
        menu = RegistrationMenu(session_id=session_id, session=session, phone_number=phone_number,
                       user_response=user_response,level=level)
        return menu.execute()

    

    
    response = ("END nothing here", 200)
    
    return HttpResponse(response, content_type='text/plain')