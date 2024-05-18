import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers
from playlist.query import query
from django.http import JsonResponse, HttpResponseNotFound
from supabase import create_client, Client
import os

# Create your views here.
def show_manage_playlist_berisi(request):
    return render(request, "kelola_playlist_berisi.html")



def show_manage_add_playlist(request):
    return render(request, "kelola_tambah_playlist.html")

def show_see_detail_playlist(request):
    return render(request, "lihat_detail_playlist.html")



def add_song_to_playlist(request):
    return render(request, "add_song_to_playlist.html")

# ____________________________________________
from collections import namedtuple
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
try:
    connection = psycopg2.connect(user="postgres.kjbsshuatchylgygwyzo",
                        password="marmut-basdat",
                        host="aws-0-ap-southeast-1.pooler.supabase.com",
                        port="5432",
                        database="postgres")

    # Create a cursor to perform database operations
    connection.autocommit = True
    cursor = connection.cursor()
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

def r_detail_song(id_song):
    query = f"""
    SELECT
        K.judul,
        STRING_AGG(DISTINCT G.genre, ', ') AS genres,
        A.nama AS artist_nama,
        K.durasi,
        K.tanggal_rilis,
        K.tahun,
        S.total_play,
        S.total_download,
        ALBUM.judul AS album_judul,
        STRING_AGG(SW_AKUN.nama, ', ') AS songwriters
    FROM
        KONTEN AS K
        JOIN GENRE AS G ON K.id = G.id_konten
        JOIN SONG AS S ON K.id = S.id_konten
        JOIN ALBUM ON ALBUM.id = S.id_album
        JOIN ARTIST AS AR ON S.id_artist = AR.id
        JOIN AKUN AS A ON AR.email_akun = A.email
        JOIN SONGWRITER_WRITE_SONG AS SWS ON S.id_konten = SWS.id_song
        JOIN SONGWRITER AS SW ON SWS.id_songwriter = SW.id
        JOIN AKUN AS SW_AKUN ON SW.email_akun = SW_AKUN.email
    WHERE
        S.id_konten = '{id_song}'
    GROUP BY
        K.judul,
        A.nama,
        K.durasi,
        K.tanggal_rilis,
        K.tahun,
        S.total_play,
        S.total_download,
        ALBUM.judul;
    """
    return query

def show_song_detail(request, id_song):
    cursor = connection.cursor()
    cursor.execute(r_detail_song(id_song))
    r_detail_song_string = cursor.fetchall()

    context = {
        'detail_song': r_detail_song_string,
    }
    return render(request, "song_detail.html", context)

def r_user_playlist_detail_info(id_playlist):
    query = f"""
    SELECT up.judul, up.email_pembuat, up.jumlah_lagu, up.total_durasi, up.tanggal_dibuat, up.deskripsi
    FROM USER_PLAYLIST up
    WHERE up.id_playlist = '{id_playlist}';
    """
    return query

def r_user_playlist_detail_song(id_playlist):
    query = f"""
    SELECT K.judul, A.nama, K.durasi, K.id
    FROM PLAYLIST_SONG as PS, SONG as S, KONTEN as K,ARTIST as AR, AKUN as A
    WHERE (PS.id_song = S.id_konten AND S.id_konten = K.id AND S.id_artist = AR.id AND AR.email_akun = A.email AND PS.id_playlist = '{id_playlist}');
    """
    return query

def show_manage_playlist_kosong(request):
    return render(request, "kelola_playlist.html")

def show_manage_detail_playlist(request, id_playlist):
    cursor = connection.cursor()
    cursor.execute(r_user_playlist_detail_info(id_playlist))
    r_user_playlist_detail_info_String = cursor.fetchall()

    cursor = connection.cursor()
    cursor.execute(r_user_playlist_detail_song(id_playlist))
    r_user_playlist_detail_song_String = cursor.fetchall()
    context = {
        'user_playlist_detail_info': r_user_playlist_detail_info_String,
        'user_playlist_detail_song': r_user_playlist_detail_song_String
    }
    return render(request, "kelola_detail_playlist.html", context)

def r_user_playlist(request):
    string = f"""
    SELECT up.judul, up.jumlah_lagu, up.total_durasi, up.id_playlist
    FROM USER_PLAYLIST up
    WHERE up.email_pembuat = '{request.session.get('email')}';
    """
    hasil = query(string)
    return JsonResponse(hasil, safe=False)





# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.utils import timezone
# from .models import UserPlaylist
# from .forms import UserPlaylistForm

# @login_required
# def user_playlist_list(request):
#     user_playlists = UserPlaylist.objects.filter(email_pembuat=request.user.email)
#     last_login = request.COOKIES.get('last_login', '')
#     context = {
#         'user_playlists': user_playlists,
#         'last_login': last_login,
#         'user': request.user.username,
#     }
#     return render(request, 'user_playlist_list.html', context)

# @login_required
# def user_playlist_create(request):
#     if request.method == 'POST':
#         form = UserPlaylistForm(request.POST)
#         if form.is_valid():
#             user_playlist = form.save(commit=False)
#             user_playlist.email_pembuat = request.user.email
#             user_playlist.tanggal_dibuat = timezone.now().date()
#             user_playlist.save()
#             return redirect('user_playlist_list')
#     else:
#         form = UserPlaylistForm()
#     context = {
#         'form': form,
#         'user': request.user.username,
#     }
#     return render(request, 'user_playlist_form.html', context)

# @login_required
# def user_playlist_update(request, pk):
#     user_playlist = get_object_or_404(UserPlaylist, pk=pk, email_pembuat=request.user.email)
#     if request.method == 'POST':
#         form = UserPlaylistForm(request.POST, instance=user_playlist)
#         if form.is_valid():
#             form.save()
#             return redirect('user_playlist_list')
#     else:
#         form = UserPlaylistForm(instance=user_playlist)
#     context = {
#         'form': form,
#         'user_playlist': user_playlist,
#         'user': request.user.username,
#     }
#     return render(request, 'user_playlist_form.html', context)

# @login_required
# def user_playlist_delete(request, pk):
#     user_playlist = get_object_or_404(UserPlaylist, pk=pk, email_pembuat=request.user.email)
#     if request.method == 'POST':
#         user_playlist.delete()
#         return redirect('user_playlist_list')
#     context = {
#         'user_playlist': user_playlist,
#         'user': request.user.username,
#     }
#     return render(request, 'user_playlist_delete.html', context)