import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photobook.settings')

app = Celery('photobook')
app.config_from_object('django.conf:settings')
app.conf.timezone = 'Europe/Moscow'

app.conf.beat_schedule = {
    'send-email-daily_top3': {
        'task': 'app.tasks.choice_top_3',
        'schedule': crontab(minute=5, hour=9),
        'args': ('daily',)
    },
    'send-email-monthly_top3': {
        'task': 'app.tasks.choice_top_3',
        'schedule': crontab(minute=0, hour=9, day_of_month='1'),
        'args': ('monthly',)
    }
}

app.autodiscover_tasks()
