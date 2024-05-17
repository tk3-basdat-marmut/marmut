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
from django.http import JsonResponse


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

def r_royalti(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("royalti").select("*").execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

