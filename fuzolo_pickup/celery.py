from __future__ import absolute_import, unicode_literals
from argparse import Namespace
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fuzolo_pickup.settings')

app = Celery('fuzolo_pickup')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings, namespace = 'CELERY')
app.conf.beat_schedule = {
    'confirm-game' : {
        'task' : 'fuzolo_pickup.task.confirm_game',
        'schedule' : crontab
    }
}

#Celery Beat Settings 


app.autodiscover_tasks()

@app.task(behind = True)
def debug_task(self):
    print(f'Request : {self.request!r}')