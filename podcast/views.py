from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import RssSerializer, EpisodeSerializer
from .models import Rss, Episode
# Create your views here.


class RssListView(ListAPIView):
    queryset = Rss.objects.all()
    serializer_class = RssSerializer


class EpisodeListView(ListAPIView):
    queryset = Episode.objects.all()
    serializer_class = RssSerializer



