from ast import Break
from email.policy import default
from wsgiref import headers
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import requests

headers = {"Content-type": "application/json"}
userurl = "http://localhost:3000/users"


def reverse_rev(string):
  rstring = ''.join(reversed(string))
  return rstring




@csrf_exempt
def url_callback(request):
  if request.method == 'POST':
    session_id = request.POST.get('sessionId')
    service_code = request.POST.get('serviceCode')
    phone_number = request.POST.get('phoneNumber')
    text = request.POST.get('text')

    text_length = len(text)
    omang_number = text[2:10]
    name = text[11:] if len(text) > 0 else ""
    pin = text[text_length-1:text_length-6] if name in text else ""
    print(text[1:5])
    print(reverse_rev(text[1:9]))
    print(text_length)
    #print(text[text_length-1:text_length-6])
    
    response = ""
    if text == "":
      response = "CON Welcome to 1Gov \n"
      response += "1. Citizen Registration \n"
      response += "2. Non-Citizen Registration \n"
      response += "3. Login "
      
    ############--CITIZEN REGISTRATION START--#####

    elif text == "1":
      response = "CON Enter Your ID(Omang) Number "
      

    #elif "1*" in text and len(text) == 11 and method1Executed:
    elif "1*" in text and len(text) == 11:
      print("method2")
      omang_number = text[2:]
      data = requests.get(userurl)
      users = data.json()
      for user in users:
        stringid = str(user['idNumber'])
        if len(stringid) < 9 :
          response = "END Invalid ID Number length"
          
        elif str(user['idNumber']) != omang_number:
          response = "END Invalid ID Number"
      
        elif omang_number.isnumeric: 
          response = f"CON User {omang_number} Enter Your Full Name"
          continue
          
          
     
    elif omang_number in text and name in text and not pin:
      
      name = text[11:]
      response = f"CON Create {pin} Your 4-Digit Pin"
      


    elif omang_number and pin in text:
      
      response = f"CON Verify Your 4-Digit Pin"


    elif text.startswith(f'1*{omang_number}*{name}*{pin}'):
      verify_pin = text[-1:-5]
      if pin == verify_pin:

        response = f"END Welcome to 1Gov Services {name} \n"
        response += "1. License Renewal \n"
        response += "2. Goverment Sponsorship"

    ############--CITIZEN REGISTRATION END--#####
    elif text == "1*1":
      response = "CON You will be charged N100 for your Daily Sports news subscription \n"
      response += "1. Auto-Renew \n"
      response += "2. One-off Purchase \n"
      
    elif text == "1*1*1":
      response = "END thank you for subscribing to our daily sport news plan \n"

    elif text == "1*1*2":
      response = "END thank you for your one-off daily sport news plan \n"

    elif text == "1*2":
      response = "CON You will be charged N50 for our weekly Sports news plan \n"
      response += "1. Auto-Renew \n"
      response += "2. One-off Purchase \n"
     
    elif text == "1*2*1":
      response = "END thank you for subscribing to our weekly sport news plan \n"

    elif text == "1*2*2":
      response = "END thank you for your one-off weekly sport news plan \n"

    elif text == "1*3":
      response = "CON You will be charged N25 for our monthly Sports news plan \n"
      response += "1. Auto-Renew \n"
      response += "2. One-off Purchase \n"
     
    elif text == "1*3*1":
      response = "END thank you for subscribing to our monthly sport news plan \n"

    elif text == "1*3*2":
      response = "END thank you for your one-off monthly sport news plan \n"

    return HttpResponse(response, content_type='text/plain')