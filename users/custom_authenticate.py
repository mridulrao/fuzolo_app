from django.contrib.auth.backends import BaseBackend
from .models import FuzoloUser  

class PhoneBackend(BaseBackend):
    def authenticate(self, request, phone_number=None):
        try:
            user = FuzoloUser.objects.get(phone_number=phone_number)
            return user
        except FuzoloUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return FuzoloUser.objects.get(pk=user_id)
        except FuzoloUser.DoesNotExist:
            return None
