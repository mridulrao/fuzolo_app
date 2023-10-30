from cmath import nan
from fuzolo_pickup.settings import RZP_REDIRECT
from users.models import FuzoloUser, FuzoloUserDetails
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .users_internal import send_otp, verify_otp, create_user, check_profile, get_user_details
from .razorpay_internal import get_payment_details, verify_payment_status, user_rzp_transactions, verify_user_rzp_transactions
from django.views.decorators.csrf import csrf_exempt

#celery_task
#from fuzolo_pickup.task import add_points_to_user
from .users_internal import add_points_to_user

def mobile_login(request):
    if request.method == 'POST':
        if 'mobile-number' in request.POST:
            mobile = request.POST.get('mobile-number')
            send_otp(request, mobile)
            return render(request, 'users/otp_login.html')

    return render(request, 'users/mobile_login.html')


def otp_verify(request):
    if request.method == 'POST':
        if 'otp' in request.POST:
            otp = request.POST.get('otp')
            phone_number = request.session.get('phone-number')
            if verify_otp(request, otp):
                if create_user(request):
                    return render(request, 'users/create_profile.html', {'phone_number' : phone_number})
                else:
                    if check_profile(request):
                        new_user = authenticate(request, phone_number = phone_number)
                        login(request, new_user)
                        print(request.user)
                        user_details = get_user_details(new_user)
                        return render(request, 'users/profile.html', {'user_details' : user_details})
                    else:
                        return render(request, 'users/create_profile.html', {'phone_number' : phone_number})

            else:
                print('Verification unsuccessful')

    return render(request, 'users/mobile_login.html')


@login_required
def profile(request):
    try:
        user = get_user_details(request.user)
    except:
        return redirect('mobile-login')
    return render(request, 'users/profile.html', {'user_details' : user})


@login_required
def add_points(request):
    if request.method == 'POST':
        user_details = get_user_details(request.user)
        if '300' in request.POST:
            payment_details = get_payment_details('300')
            user_rzp_transactions(user_details, payment_details, '300')           
            return render(request, 'users/add_points.html', {'user_details' : user_details, 'payment_details' : payment_details, 'redirect_url' : RZP_REDIRECT})
        elif 'basic-plan' in request.POST:
            payment_details = get_payment_details('2850')
            user_rzp_transactions(user_details, payment_details, '2850')
            return render(request, 'users/add_points.html', {'user_details' : user_details, 'payment_details' : payment_details, 'redirect_url' : RZP_REDIRECT})

    return render(request, 'users/profile.html')

@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        payment_details = {
            'payment_id' : request.POST['razorpay_payment_id'],
            'order_id' : request.POST['razorpay_order_id'],
            'signature' : request.POST['razorpay_signature']
        }
        flag_rzp = verify_payment_status(payment_details)
        flag_fuzolo, amount = verify_user_rzp_transactions(payment_details['order_id'])

        if flag_rzp and flag_fuzolo:
            user = str(FuzoloUserDetails.objects.get(phone_number = request.user).phone_number)
            points = int(amount)
            add_points_to_user(user, points)
            #add_points_to_user.apply_async(args = [user, points])
            #logout(request)
            return redirect('profile')
        else:
            print("Payment Verification Failed")
    
    return render(request, 'users/verify_payments.html')


def custom_plans(request):
    return render(request, 'users/custom_plans.html')