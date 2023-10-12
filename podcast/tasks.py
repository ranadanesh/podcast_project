from abc import ABC
from .models import Rss
from .parser import parserview
from celery import shared_task, Task



class BasePodcastTask(Task, ABC):
    retry_backoff = 2
    jitter = True


@shared_task(base=BasePodcastTask, bind=True)
def update_podcast_task(self, url):
    parserview(url)


