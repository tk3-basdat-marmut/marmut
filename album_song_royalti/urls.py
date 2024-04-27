from django.urls import path
from album_song_royalti.views import dashboard, r_album

app_name = 'album_song_royalti'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('r_album', r_album, name='r-album'),
]