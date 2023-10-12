from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import RssSerializer, EpisodeSerializer
from .models import Rss, Episode
from .parser import parserview
# Create your views here.


class RssListView(ListAPIView):
    queryset = Rss.objects.all()
    serializer_class = RssSerializer


class EpisodeListView(ListAPIView):
    queryset = Episode.objects.all()
    serializer_class = RssSerializer


class RssDetailView(APIView):

    def get(self, request, pk):
        rss = get_object_or_404(Rss, pk=pk)
        serializer = RssSerializer(rss)
        return Response(serializer.data)


class EpisodeDetailView(APIView):

    def get(self, request, pk):
        episode = get_object_or_404(Episode, pk=pk)
        serializer = EpisodeSerializer(episode)
        return Response(serializer.data)


class ParseUrl(APIView):
    def post(self, request):
        url = request.data.get("rss_url")
        # print(url)
        parserview(url)
        return Response("Podcast Updated", status=201)
