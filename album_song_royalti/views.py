from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import render
import os
from supabase import create_client, Client
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
import json
from django.http import JsonResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
import uuid




def dashboard(request):
    context = {
        'name': '.....',
        'class': '....',
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "album_song_royalti_dashboard.html", context)

def r_album(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("album").select("*").execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def c_album(request):
    return None

def d_album(request):
    return None

def u_album(request):
    return None

def r_song(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("song").select("*").execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def r_song2(request, id_album):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("song").select("*").eq('id_album', id_album).execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def c_song(request, id_artist, id_album):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    data = supabase.table("song").insert({"id_konten": 1,
                                          "id_artist": id_artist,
                                          "id_album":id_album,
                                          "total_play": 0,
                                          "total_download":0,}).execute()
    response = data.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def r_royalti(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("royalti").select("*").execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

@csrf_exempt
def add_product_ajax(request):
    if request.method == 'POST':
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        supabase = create_client(url, key)
        id_konten = request.POST.get("id_konten")
        id_album = request.POST.get("id_album")
        id_artist = request.POST.get("id_artist")
        total_play = request.POST.get("total_play")
        total_download = request.POST.get("total_download")
        data = supabase.table("song").insert({"id_album":id_album,
                                        "id_artist": id_artist,
                                         "id_konten": id_konten,
                                        "total_play": total_play,
                                       "total_download":total_download,}).execute()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def add_content_ajax(request):
    if request.method == 'POST':
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        supabase = create_client(url, key)
        
        judul = request.POST.get("judul")
        tanggal_rilis = request.POST.get("tanggal_rilis")
        tahun = request.POST.get("tahun")
        durasi = request.POST.get("durasi")
        # Generate UUID as a string
        uuid_str = str(uuid.uuid4())

        # Insert data into the database
        data = supabase.table("konten").insert({
            "id": uuid_str,
            "judul": judul,
            "tanggal_rilis": tanggal_rilis,
            "tahun": tahun,
            "durasi": durasi,
        }).execute()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

