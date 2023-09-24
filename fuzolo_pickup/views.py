from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .fuzolo_pickup_internals import save_user_details, get_user_details, update_wallet_list
from .fuzolo_pickup_internals import get_game_details, create_game, schedule_confirm_game

from .models import Pickup, PickupPlayers
from users.models import FuzoloUser, FuzoloUserDetails

def view_pickup(request):
    if request.method == 'POST':
        if save_user_details(request):
            print("Details Saved")
            user = FuzoloUser.objects.get(phone_number = request.session.get('phone-number'))
            login(request, user, backend='users.custom_authenticate.PhoneBackend')

        #create game request
        if 'title' in request.POST:
            game_details = get_game_details(request)
            new_game = create_game(game_details)
            flag = schedule_confirm_game(game_details)

    try:
        user_details = get_user_details(request.user)
        games = Pickup.objects.all()
        return render(request, 'fuzolo_pickup/view_pickup.html', {'games' : games, 'user_details' : user_details})
    except:
        print("No Pickup games")
    
    return render(request, 'fuzolo_pickup/view_pickup.html')

def create_pickup(request):
    return render(request, 'fuzolo_pickup/create_game.html')

def details_pickup(request, game_id):
    game_details = Pickup.objects.get(game_id = game_id)
    game_players = PickupPlayers.objects.filter(game_id = game_id)
    user_details = get_user_details(request.user)

    if request.method == 'POST':
        if 'join-game' in request.POST:
            user_details = get_user_details(request.user)
            new_player = PickupPlayers.objects.create(game_id = game_details.game_id,
                                                      name = user_details['name'],
                                                      mobile = user_details['user_phone_number'],
                                                      email = user_details['email'],
                                                      manager_added = False)

            #update pickup 
            wallet_list = update_wallet_list(game_details.wallet_list, str(request.user))
            game_details.wallet_list = wallet_list
            game_details.joined_players += 1
            game_details.save()

        if 'delete-game' in request.POST:
            print("Delete Game")

        if 'join-waitlist' in request.POST:
            print("Join Waitlist")

    return render(request, 'fuzolo_pickup/details_game.html', {'game_details' : game_details, 'game_players' : game_players, 'user_details' : user_details})