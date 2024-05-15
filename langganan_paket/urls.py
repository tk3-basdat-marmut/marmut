from django.urls import path
from .views import r_list_packages, c_subscribe_to_package, r_transaction_history, search_content, r_downloaded_songs, d_downloaded_songs, song_detail

urlpatterns = [
    path('packages/', r_list_packages, name='r-list-packages'),
    path('subscribe/', c_subscribe_to_package, name='c-subscribe-to-package'),
    path('history/<str:email>/', r_transaction_history, name='r-transaction-history'),
    path('search/', search_content, name='search-content'),
    path('downloaded-songs/', r_downloaded_songs, name='r-downloaded-songs'),
    path('song-detail/<uuid:id_song>/', song_detail, name='song_detail'),
    path('delete-song/<uuid:id_song>/', d_downloaded_songs, name='d-downloaded-songs'),
]
