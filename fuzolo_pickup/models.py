from django.db import models

class Pickup(models.Model):
    title = models.CharField(max_length = 50)
    game_id = models.CharField(max_length = 50)
    day = models.CharField(max_length = 20)
    date = models.DateField()
    duration = models.IntegerField()
    start_time = models.CharField(max_length = 20)
    end_time = models.CharField(max_length = 20)
    reporting_time = models.CharField(max_length = 20)
    max_players = models.IntegerField()
    price_per_player = models.IntegerField()
    hourly_price = models.IntegerField()
    joined_players = models.IntegerField()
    waiting_list = models.CharField(max_length = 200)
    wallet_list = models.CharField(max_length = 200)
    venue = models.CharField(max_length = 200)

    def __str__(self):
        return self.game_id
    
class PickupPlayers(models.Model):
    game_id = models.CharField(max_length = 50)
    name = models.CharField(max_length = 50)
    mobile = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    remark = models.CharField(max_length = 20, default = 'No Show')
    present = models.BooleanField(default = False)
    present_timestamp = models.DateTimeField(auto_now = True)
    manager_added = models.BooleanField(default = True)

    def __str__(self):
        return self.game_id