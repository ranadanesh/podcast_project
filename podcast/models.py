from django.db import models
# from core import models as core_model
# Create your models here.


class Rss(models.Model):
    url = models.URLField()
    link = models.URLField()
    title = models.CharField(max_length=200)
    email = models.CharField(max_length=150)
    owner = models.CharField(max_length=50)
    summary = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=255)
    narrator = models.CharField(max_length=200)
    copyright = models.CharField(max_length=200)
    explicit = models.CharField(max_length=200)
    language = models.CharField(max_length=20)


class Episode(models.Model):
    rss = models.ForeignKey(Rss, on_delete=models.CASCADE)
    guid = models.CharField(max_length=50, unique=True)
    enclosure = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=200)
    duration = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200)
    audio_file = models.CharField(max_length=200, null=True, blank=True)
    publish_date = models.CharField(max_length=200)
    explicit = models.CharField(max_length=200)
    summary = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=50, blank=True, null=True)
    keyword = models.CharField(max_length=200)
    image = models.CharField(max_length=255)
