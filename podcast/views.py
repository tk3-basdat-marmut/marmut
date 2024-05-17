from dotenv import load_dotenv
from podcast import query
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
# from .asdf import fetch_podcast_details
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
from album_song_royalti.query import query

# Create your views here.
def dashboard(request):
    context = {
        
            'status': request.session.get('status'),
            'nama': request.session.get('nama'),
            'last_login': request.COOKIES['last_login'],
    }

    return render(request, "podcast.html", context)

def r_podcast(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("podcast_detail_list").select("*").execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def r_podcast_detail(request, id):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("podcast_view").select("*").eq('id', id).execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def r_episode(request, id_konten_podcast):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("episode").select("*").eq('id_konten_podcast', id_konten_podcast).execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

# def r_podcast(request):
#     details_list = fetch_podcast_details()
#     # return JsonResponse(response, safe=False)
#     return render(request, 'podcast.html', {'details_list': details_list})

# def r_podcast(request):
#     url = os.environ.get("SUPABASE_URL")
#     key = os.environ.get("SUPABASE_KEY")
#     supabase = create_client(url, key)
#     test = supabase.table("podcast").select("*").execute()
#     response = test.data
#     # Convert dictionary to JSON response
#     return JsonResponse(response, safe=False)

def r_chart(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("chart").select("*").execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def rd_episode(request):
    return render(request, "episode_list.html")

def c_podcast(request):
    return render(request, "create_podcast.html")

def r_play_podcast(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("episode").select("*").execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def show_play_podcast(request):
    return render(request, "podcast_detail.html")

def list_podcast(request):
    return render(request, "podcast2.html")

# @csrf_exempt
# def add_episode_ajax(request):
#     if request.method == 'POST':
#         url = os.environ.get("SUPABASE_URL")
#         key = os.environ.get("SUPABASE_KEY")
#         supabase = create_client(url, key)
        
#         id_podcast = request.POST.get("id_podcast")
#         judul_episode = request.POST.get("judul_episode")
#         deskripsi_episode = request.POST.get("deskripsi_episode")
#         durasi_episode = request.POST.get("durasi_episode")

#         # Generate UUID as a string
#         uuid_episode = str(uuid.uuid4())

#         episode = supabase.table("episode").insert({
#             "id_episode": uuid_episode,
#             "id_konten_podcast": id_podcast,
#             "judul": judul_episode,
#             "deskripsi": deskripsi_episode,
#             "durasi": durasi_episode,
#             "tanggal_rilis": datetime.datetime.now().strftime("%Y-%m-%d")
#         }).execute()

#         selected_podcast = supabase.table("podcast_detail").select("*").eq('id_konten', id_podcast).execute()
#         jumlah_episode = selected_podcast.data[0]['jumlah_episode'] + 1
#         total_durasi = selected_podcast.data[0]['total_durasi'] + int(durasi_episode)
#         string = f"UPDATE podcast_detail SET jumlah_episode = {jumlah_episode}, total_durasi = {total_durasi} WHERE id_konten = '{id_podcast}';"
#         hasil = query(string)

#         return HttpResponse(b"CREATED", status=201)

#     return HttpResponseNotFound()

# # def r_play_podcast(request):
# #     return render(request, "podcast_detail.html")