from django.contrib import admin


from .models import FuzoloUser
class FuzoloUserClass(admin.ModelAdmin):
    list_display = ('phone_number', 'is_staff', 'pickup_manager')
admin.site.register(FuzoloUser, FuzoloUserClass)

from .models import FuzoloUserDetails
class FuzoloUserDetailsClass(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'date_joined', 'points')
admin.site.register(FuzoloUserDetails, FuzoloUserDetailsClass)