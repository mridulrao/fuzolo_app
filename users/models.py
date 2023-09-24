from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from fuzolo_pickup import settings

#managers
from .managers import CustomUserManager

class FuzoloUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=10, unique=True)
    is_verified = models.BooleanField(default=True)

    #managers
    pickup_manager = models.BooleanField(default = False)

    #superuser 
    is_staff = models.BooleanField(default=False) #required for admin
    is_superuser = models.BooleanField(default = False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number


class FuzoloUserDetails(models.Model):
    name = models.CharField(max_length = 255)
    email = models.EmailField()
    phone_number = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(default=timezone.now)
    points = models.IntegerField(default = 0)
    email_verified = models.BooleanField(default = False)

    #memberships
    footbal_membership_id = models.CharField(max_length = 255, default = '--')
    cricket_membership_id = models.CharField(max_length = 255, default = '--')

    def __str__(self):
        return self.name
