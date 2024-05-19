from django.urls import path
from playlist.views import *

app_name = 'playlist'

urlpatterns = [
    # HTML View
    # Playlist manage
    path('manage-playlist', show_manage_playlist, name='show_manage_playlist'),
    path('manage-detail-playlist/<str:id_playlist>/', show_manage_detail_playlist, name='show_detail_playlist'),
    path('manage-add-playlist/<str:id_playlist>/', show_manage_add_playlist, name='show_detail_playlist'),
    path('manage-add-playlist/<str:id_playlist>/', show_manage_add_playlist, name='show_detail_playlist'),

    # Playlist see
    path('see-detail-playlist/<str:id_playlist>/', show_see_detail_playlist, name='show_detail_playlist'),

    # Song
    path('see-detail-song/<str:id_song>/', show_song_detail, name='r_detail_song'),
    path('song/add/<str:id_song>/', add_song_to_playlist_Frontend, name='show_detail_playlist'),


    path('r-user-playlist', r_user_playlist, name='r_user_playlist'),
    path('add-song-to-playlist', add_song_to_playlist, name='add_song_to_playlist'),
    path('play-song', play_song, name='play_song'),
    path('delete-song-from-playlist', delete_song_from_playlist, name='delete_song_from_playlist'),

    # Fetching needs
    path('fetch-songs', fetch_song, name='fetch_song'),
    path('fetch-my-playlist', fetch_my_playlist, name='fetch_my_playlist'),


]