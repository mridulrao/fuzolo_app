from unicodedata import name
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import mobile_login, otp_verify, profile, add_points, verify_payment


urlpatterns = [
    #auth logout
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    #user views
    path('mobile_login/', mobile_login, name='mobile-login'),
    path('verify_otp/', otp_verify, name = 'otp-verify'),
    path('profile/', profile, name = 'profile'),
    path('add_points/', add_points, name = 'add-points'),
    path('verify_payment/', verify_payment, name = 'verify-payment')
]