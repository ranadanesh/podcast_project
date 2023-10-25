from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'update_podcast_every_hour': {
        'task': 'podcast.tasks.update_podcast_task',
        'schedule': crontab(hour="*/1")  # */1 -> every hour,minutes = */1 -> every minutes
    }

}