import random
from sndhdr import what
from users.models import FuzoloUser, FuzoloUserDetails

from .whatsapp_users import whatsapp_otp
from .twilio_internal import send_otp_via_message

def send_otp(request, phone_number):
    otp = str(random.randint(100000, 999999))
    request.session['mobile-otp'] = otp
    request.session['phone-number'] = phone_number
    #print(otp)
    details = {
        'text1' : 'Login OTP',
        'otp' : otp,
        'text2' : 'otp',
        'phone_no' : phone_number 
    }

    whatsapp_otp(details)
    #send_otp_via_message(details)

def verify_otp(request, entered_otp):
    generated_otp = request.session.get('mobile-otp')

    if generated_otp == entered_otp:
        del request.session['mobile-otp']
        return True

    return False

def create_user(request):
    phone_number = request.session['phone-number']
    try:
        user = FuzoloUser.objects.get(phone_number = phone_number)
        return False

    except:
        user = FuzoloUser.objects.create(phone_number=phone_number, is_verified=True)

    return True

def check_profile(request):
    phone_number = request.session.get('phone-number')
    try:
        user_phone_number = FuzoloUser.objects.get(phone_number = phone_number)
        user_details = FuzoloUserDetails.objects.get(phone_number = user_phone_number)
        return True
    except:
        return False


def get_user_details(user):
    user_details = FuzoloUserDetails.objects.get(phone_number = user)
    user_details_dict = {
        'name' : user_details.name,
        'email' : user_details.email,
        'phone_number' : user_details.phone_number,
        'points' : user_details.points
    }

    return user_details_dict

