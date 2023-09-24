import requests
import json


def whatsapp_otp(details):
    url = "https://api.interakt.ai/v1/public/message/"
    headers = {
        "Authorization": "Basic ZUczMmRPb3hmakg3QUNTT0lzcTdweWRyYjlqSWdTOVE2SU1uY0JsdGd0azo=",
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