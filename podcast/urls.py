from django.urls import path
from .parser import parserview
from .views import RssListView, EpisodeListView, RssDetailView, EpisodeDetailView

urlpatterns = [
    path('parse/', parserview),
    path('rss/', RssListView.as_view(), name='rss'),
    path('episode/', EpisodeListView.as_view(), name='episode'),
    path('rss/<int:pk>/', RssDetailView.as_view(), name='rss-detail'),
    path('episode/<int:pk>/', EpisodeListView.as_view(), name='episode-detail'),
]
