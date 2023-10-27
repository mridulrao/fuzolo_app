import requests
import json
from fuzolo_pickup.settings import WHASTSAPP_KEY 

manager_number = ['9599445661']

def notify_manager():
    for phone_number in manager_number:
        url = "https://api.interakt.ai/v1/public/message/"
        headers = {
            "Authorization": WHASTSAPP_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "countryCode": "+91",
            "phoneNumber": phone_number,
            "callbackData": "Testing Mridul, FUZOLO",
            "type": "Template",
            "template": {
                "name": "notify_manager",
                "languageCode": "en",
                "bodyValues": []
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))


def notify_players(game_players, game_details):
    names = [player.name for player in game_players]
    mobile_numbers = [player.mobile for player in game_players]
    for (name, number) in zip(names, mobile_numbers):

        url = "https://api.interakt.ai/v1/public/message/"
        headers = {
            "Authorization": WHASTSAPP_KEY,
            "Content-Type": "application/json"
        }
        payload = {
            "countryCode": "+91",
            "phoneNumber": str(number),
            "callbackData": "Testing Mridul, FUZOLO",
            "type": "Template",
            "template": {
                "name": "notify_players",
                "languageCode": "en",
                "headerValues": [
                    str(name)
                ],
                "bodyValues": [
                    str(game_details.start_time),
                    str(game_details.date)
                ]
            }
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
