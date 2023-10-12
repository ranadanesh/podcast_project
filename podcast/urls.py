from django.urls import path
from .parser import parserview
from .views import RssListView, EpisodeListView, RssDetailView, EpisodeDetailView, ParseUrl

urlpatterns = [
    path('parse/', ParseUrl.as_view(), name='parse'),
    path('rss/', RssListView.as_view(), name='rss'),
    path('episode/', EpisodeListView.as_view(), name='episode'),
    path('rss/<int:pk>/', RssDetailView.as_view(), name='rss-detail'),
    path('episode/<int:pk>/', EpisodeListView.as_view(), name='episode-detail'),
]
