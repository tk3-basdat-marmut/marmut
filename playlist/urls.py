from django.urls import path
from playlist.views import *

app_name = 'playlist'

urlpatterns = [
    path('front-end/manage-playlist-berisi', show_manage_playlist_berisi, name='show_playlist_berisi'),
    path('front-end/manage-playlist-kosong', show_manage_playlist_kosong, name='show_playlist_kosong'),
    path('front-end/manage-detail-playlist', show_manage_detail_playlist, name='show_detail_playlist'),
    path('front-end/manage-add-playlist', show_manage_add_playlist, name='show_detail_playlist'),

    path('front-end/see-detail-playlist', show_see_detail_playlist, name='show_detail_playlist'),

    path('front-end/see-song-detail', show_song_detail, name='show_detail_playlist'),
    path('front-end/add-song-to-playlist', add_song_to_playlist, name='show_detail_playlist'),

]