'''
from django.conf import settings
from twilio.rest import Client
from fuzolo_pickup.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_COUNTRY_CODE, TWILIO_PHONE_NUMBER

def send_otp_via_message(details): 
    body_message = f"Hi! Your FUZOLO OTP is {details['otp']}"    
    client= Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(body = body_message,
                                    from_ = TWILIO_PHONE_NUMBER,
                                    to = f"{TWILIO_COUNTRY_CODE}{details['phone_no']}")'''