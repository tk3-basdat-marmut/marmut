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
        # 'last_login': request.COOKIES['last_login'],
    }

    return render(request, "chart.html", context)

def r_chart(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("chart").select("*").execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def r_specific_chart(request, id_playlist):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("chart").select("*").eq('id_playlist', id_playlist).execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def r_chart_view(request, id):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("chart_list").select("*").eq('id', id).execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def chart_detail(request):
    return render(request, "chart_detail.html")

def d_song(request, id_song):
    if request.method == 'GET':   
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        supabase = create_client(url, key)
        
        # Delete the record with the specified id_album and let cascading delete handle associated records
        # song = supabase.table('song').select('*').eq('id_konten', id_konten).execute()
        # konten = supabase.table('konten').select('*').eq('id', id_konten).execute()

        # album = supabase.table('album').select('*').eq('id', song.data[0]['id_album']).execute()

        response = supabase.table('playlist_song').delete().eq('id_song', id_song).execute() 
        #jumlah_sekarang = album.data[0]['jumlah_lagu'] - 1
        #durasi_sekarang = album.data[0]['total_durasi'] - int(konten.data[0]['durasi'])
        #string = f"UPDATE album SET jumlah_lagu = {jumlah_sekarang}, total_durasi = {durasi_sekarang} WHERE id = '{album.data[0]['id']}';"
        #hasil = query(string)
        
        return HttpResponse(b"CREATED", status=201)
    