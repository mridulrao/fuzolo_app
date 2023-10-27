import email
from time import time
from users.models import FuzoloUserDetails, FuzoloUser
from datetime import datetime, timedelta
from django.utils.crypto import get_random_string
import math

from .models import Pickup, PickupPlayers
from datetime import datetime, timedelta

#celery task 
from .task import check_confirm_game


def save_user_details(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone_number = request.session.get('phone-number')

    try:
        user_phone_number = FuzoloUser.objects.get(phone_number = phone_number)

        try:
            user_details = FuzoloUserDetails.objects.create(id = None,
                                                        name = name,
                                                        email = email,
                                                        phone_number = user_phone_number)
        except:
            print("User details already saved")

        return True

    except:
        print("User details cannot be saved")

    return False

def get_user_details(user):
    fuzolo_user_details = FuzoloUserDetails.objects.get(phone_number = user)
    user_details = {
        'logged_in' : False,
        'pickup_manager' : False,
        'user_points' : 0,
        'user_phone_number' : '',
        'name' : '',
        'email' : ''
    }

    if str(user) != 'AnonymousUser':
        #logged in
        user_details['logged_in'] = True
        user_details['user_phone_number'] = str(user)
        user_details['name'] = fuzolo_user_details.name
        user_details['email'] = fuzolo_user_details.email

        #check manager
        if user.pickup_manager:
            user_details['pickup_manager'] = True

        #check points
        user_details['user_points'] = int(fuzolo_user_details.points)

    else:
        print("User is anonymous")

    return user_details


def update_wallet_list(wallet_list, user_phone_number):
    wallet_list = str(wallet_list)
    wallet_list += ',' + user_phone_number
    return wallet_list


def calculate_duration_and_reporting_time(start_time, end_time):
    format_str = '%H:%M'
    start_datetime = datetime.strptime(start_time, format_str)
    end_datetime = datetime.strptime(end_time, format_str)

    if end_datetime < start_datetime:
        end_datetime = end_datetime.replace(day = end_datetime.day + 1)

    duration = end_datetime - start_datetime
    hours = duration.seconds // 3600

    report_datetime = start_datetime - timedelta(minutes = 15)

    return hours, report_datetime.strftime(format_str)


def find_day_from_date(date_str):
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    format_str = '%Y-%m-%d'
    date_object = datetime.strptime(date_str, format_str)

    day_of_week = date_object.weekday()

    return days[day_of_week]

def convert_to_12_hours(time_str):
    format_str = '%H:%M'
    time_object = datetime.strptime(time_str, format_str)
    formatted_time = time_object.strftime("%I:%M %p")

    return formatted_time

def check_fees_and_price(entry_fees, hourly_price, duration, max_players):
    if int(entry_fees) != 0:
        return entry_fees, '0'
    else:
        total_price = int(hourly_price)*int(duration)
        entry_fees = total_price/int(max_players)
        return math.ceil(entry_fees), hourly_price

def generate_unique_id():
    new_id = get_random_string(8)
    return new_id

def get_game_details(request):
    #request variable
    title = request.POST['title']
    date = request.POST['date']
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']
    max_players = request.POST['max_players']
    entry_fees = request.POST['price_per_player'] #price_per_player
    hourly_price = request.POST['hourly_price']


    #zero initialized variables
    joined_players = 0
    waiting_list = ''
    wallet_list = ''
    venue = 'FUZOLO'

    #calculated variables
    game_id = generate_unique_id()
    duration, reporting_time = calculate_duration_and_reporting_time(start_time, end_time)
    day = find_day_from_date(date)

    #check entry fees and hourly price
    entry_fees, hourly_price = check_fees_and_price(entry_fees, hourly_price, duration, max_players)

    details = {
        'title' : title,
        'date' : date, 
        'day' : day,
        'start_time' : str(convert_to_12_hours(start_time)),
        'end_time' : str(convert_to_12_hours(end_time)),
        'max_players' : max_players,
        'entry_fees' : entry_fees,
        'hourly_price' : hourly_price,
        'joined_players' : joined_players,
        'waiting_list' : waiting_list,
        'wallet_list' : wallet_list,
        'venue' : venue,
        'game_id' : game_id,
        'duration' : duration,
        'reporting_time' : reporting_time,
        'day' : day
    }

    return details



def create_game(game_details):
    pickup_game = Pickup.objects.create(title = game_details['title'],
                                            game_id = game_details['game_id'],
                                            day = game_details['day'],
                                            date = game_details['date'],
                                            duration = game_details['duration'],
                                            start_time = game_details['start_time'],
                                            end_time = game_details['end_time'],
                                            reporting_time = game_details['reporting_time'],
                                            max_players = game_details['max_players'],
                                            price_per_player = game_details['entry_fees'],
                                            hourly_price = game_details['hourly_price'],
                                            joined_players = game_details['joined_players'],
                                            waiting_list = game_details['waiting_list'],
                                            wallet_list = game_details['wallet_list'],
                                            venue = game_details['venue'])

    return pickup_game

def get_schedule_time(start_time, start_date):
    start_time = datetime.strptime(start_time, '%I:%M %p')
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    # Combine start_date and start_time to create the full start datetime
    start_datetime = datetime(
        year=start_date.year,
        month=start_date.month,
        day=start_date.day,
        hour=start_time.hour,
        minute=start_time.minute
    )

    two_hours_before = start_datetime - timedelta(hours=2)
    current_time = datetime.now()
    time_remaining = two_hours_before - current_time

    hours = int(time_remaining.total_seconds() / 3600)
    minutes = int((time_remaining.total_seconds() % 3600) / 60)

    return hours, minutes

def check_confirm_game(game_id):
    game = Pickup.objects.get(game_id = game_id)
    if game.joined_players == game.max_players:
        print("Game confirm")
    else:
        print("Game Not confirm, need action")
    return True

def schedule_confirm_game(game_details):
    start_time = game_details['start_time']
    start_date = game_details['date']
    game_id = game_details['game_id']
    hours, minutes = get_schedule_time(start_time, start_date)
    print('Schedule Confirm in ')
    print(str(hours)+ ' hours')
    print(str(minutes) + ' minutes')
    task = check_confirm_game(game_id)
    return task

def deduct_points(game_players, game):
    game_points = game.price_per_player

    for player in game_players:
        player_details = FuzoloUserDetails.objects.get(email = player.email)
        player_details.points -= game_points
        player_details.save()







