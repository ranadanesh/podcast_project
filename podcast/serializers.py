from rest_framework import serializers
from .models import Rss, Episode


class RssSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rss
        fields = '__all__'


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = '__all__'
