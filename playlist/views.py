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

# Create your views here.
def show_manage_playlist_berisi(request):
    return render(request, "kelola_playlist_berisi.html")

def show_manage_playlist_kosong(request):
    return render(request, "kelola_playlist_kosong.html")

def show_manage_detail_playlist(request):
    return render(request, "kelola_detail_playlist.html")

def show_manage_add_playlist(request):
    return render(request, "kelola_tambah_playlist.html")

def show_see_detail_playlist(request):
    return render(request, "lihat_detail_playlist.html")

def show_song_detail(request):
    return render(request, "song_detail.html")

def add_song_to_playlist(request):
    return render(request, "add_song_to_playlist.html")