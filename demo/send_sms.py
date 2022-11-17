import africastalking

# TODO: Initialize Africa's Talking

africastalking.initialize(
    username='sandbox',
    api_key='0c476ef13cab0e15e6c1ee7c9905e7610feb7e23b8f49883a816988493e92b77'
)

sms = africastalking.SMS

class send_sms():

    def send(self):
        pass
        
        #TODO: Send message

    def sending(self, phone_number, first_name, id):
        # Set the numbers in international format
        recipients = [phone_number]
        # Set your message
        message = f"Hello {first_name.capitalize()} you have successfully registered on the 1Gov plartform, your 1Gov Username is {id}.";
        # Set your shortCode or senderId
        sender = "1GOV"
        try:
            response = sms.send(message, recipients, sender)
            print (response)
        except Exception as e:
            print (f'Experiencing, technical difficulties: {e}')
