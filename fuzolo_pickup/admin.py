from django.contrib import admin

#pickup model
from .models import Pickup
class PickupClass(admin.ModelAdmin):
    list_display = ("title", "game_id", "day", "date", "start_time", "price_per_player", "joined_players")
admin.site.register(Pickup, PickupClass)

from .models import PickupPlayers
class PickupPlayerClass(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'email', 'game_id', 'manager_added', 'present_timestamp')
admin.site.register(PickupPlayers, PickupPlayerClass)
