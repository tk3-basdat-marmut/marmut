from django.urls import path
from album_song_royalti.views import *

app_name = 'album_song_royalti'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('r-album', r_album, name='r_album'),
    path('r-song', r_song, name='r_song'),
    path('r-royalti', r_royalti, name='r_royalti'),
    path('r-song2/<str:id_album>/', r_song2, name='r_song2'),
    path('c_song/<str:id_artist>/<str:id_album>/', c_song, name='c_song'),
    path('d-album/<str:id_album>/', d_album, name='d_album'),
    path('add-product-ajax', add_product_ajax, name='add_product_ajax'),
    path('add-album-ajax', add_album_ajax, name='add_album_ajax'),
    path('add-content-ajax', add_content_ajax, name='add_content_ajax'),
    path('add-song-ajax', add_song_ajax, name='add_song_ajax'),
    path('fetch-labels', fetch_labels, name='fetch_labels'),
    path('fetch-genres', fetch_genres, name='fetch_genres'),
    path('fetch-artists', fetch_artists, name='fetch_artists'),
    path('fetch-songwriters', fetch_songwriters, name='fetch_songwriters'),
    path('fetch-podcasters', fetch_podcasters, name='fetch_podcasters'),
    path('fetch-episodes/<str:id_konten>/', fetch_episodes, name='fetch_episodes'),
    path('podcast-render', podcast_render, name='podcast_render'),
    path('royalti-render', royalti_render, name='royalti_render'),
    path('r-podcast', r_podcast, name='r_podcast'),
]