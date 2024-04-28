from django.urls import path
from album_song_royalti.views import dashboard, r_album, r_song, r_royalti, r_song2

app_name = 'album_song_royalti'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('r-album', r_album, name='r_album'),
    path('r-song', r_song, name='r_song'),
    path('r-royalti', r_royalti, name='r_royalti'),
    path('r-song2/<str:id_album>/', r_song2, name='r_song2'),
]