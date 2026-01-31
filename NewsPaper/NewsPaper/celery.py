import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from celery.schedules import crontab
app.conf.beat_schedule = {
    'send-weekly-digest': {
        'task': 'news.tasks.send_weekly_digest',
        'schedule': crontab(day_of_week=0, hour=8, minute=0),  # Понедельник 8:00
    },
}