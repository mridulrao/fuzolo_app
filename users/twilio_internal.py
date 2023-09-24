
from django.conf import settings
from twilio.rest import Client


ACCOUNT_SID='AC217980b3ad2707f261a6a63cb8f55df6'
AUTH_TOKEN='de527f3fca0cb1ba14b305bce3730eb7'
COUNTRY_CODE='+91'
TWILIO_WHATSAPP_NUMBER=''
TWILIO_PHONE_NUMBER='+12512204986'

def send_otp_via_message(details): 
    body_message = f"Hi! Your FUZOLO OTP is {details['otp']}"    
    client= Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(body = body_message,
                                    from_ = TWILIO_PHONE_NUMBER,
                                    to = f"{COUNTRY_CODE}{details['phone_no']}")