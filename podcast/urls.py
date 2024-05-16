from django.urls import path
from podcast.views import dashboard, r_podcast, r_chart, rd_episode, c_podcast, r_play_podcast, show_play_podcast, list_podcast, r_podcast_detail, r_episode

app_name = 'podcast'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('r-podcast', r_podcast, name='r_podcast'),
    path('r-chart', r_chart, name='r_chart'),
    path('rd-episode', rd_episode, name='rd_episode'),
    path('c-podcast', c_podcast, name='c_podcast'),
    path('r-play-podcast', r_play_podcast, name='r_play_podcast'),
    path('show-play-podcast', show_play_podcast, name='show_play_podcast'),
    path('list-podcast', list_podcast, name='list_podcast'),
    path('r-podcast-detail/<str:id>/', r_podcast_detail, name='r_podcast_detail'),
    path('r-episode/<str:id_konten_podcast>/', r_episode, name='r_episode')
]