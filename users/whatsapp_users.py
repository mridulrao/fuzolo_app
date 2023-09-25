import requests
import json
from fuzolo_pickup.settings import WHASTSAPP_KEY 


def whatsapp_otp(details):
    url = "https://api.interakt.ai/v1/public/message/"
    headers = {
        "Authorization": WHASTSAPP_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "countryCode": "+91",
        "phoneNumber": str(details['phone_no']),
        "callbackData": "Testing Mridul, FUZOLO",
        "type": "Template",
        "template": {
            "name": "fuzolo_mobile_login",
            "languageCode": "en",
            "bodyValues": [
                str(details['text1']),
                str(details['otp']),
                str(details['text2'])
            ]
        }
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.text)