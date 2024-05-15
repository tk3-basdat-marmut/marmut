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
    path('add-product-ajax', add_product_ajax, name='add_product_ajax'),
    path('add-content-ajax', add_content_ajax, name='add_content_ajax'),
]