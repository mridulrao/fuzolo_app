from unicodedata import bidirectional
from celery import shared_task
from .models import Pickup

from users import models as user_models


@shared_task(bind = True)
def check_confirm_game(self, game_id):
    game = Pickup.objects.get(game_id = game_id)
    if game.joined_players == game.max_players:
        print("Game confirm")
    else:
        print("Game Not confirm, need action")
    return True


@shared_task(bind = True)
def add_points_to_user(self, user, points):
    user = user_models.FuzoloUser.objects.get(phone_number = user)
    user_details = user_models.FuzoloUserDetails.objects.get(phone_number = user)
    try:
        user_details.points += int(points)
        user_details.save()
        print("Points added")
    except:
        print("User points cannot be updated")


