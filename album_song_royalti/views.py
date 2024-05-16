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




def dashboard(request):
    if request.session.get('status') == 'Label':
        context = {
            'status': request.session.get('status'),
            'nama': request.session.get('nama'),
            'last_login': request.COOKIES['last_login'],
        }
        return render(request, "album_song_royalti_dashboard_label.html", context)
    else:
        context = {
            'status': request.session.get('status'),
            'nama': request.session.get('nama'),
            'last_login': request.COOKIES['last_login'],
        }
        return render(request, "album_song_royalti_dashboard.html", context)

def podcast_render(request):
    context = {
        'status': request.session.get('status'),
        'nama': request.session.get('nama'),
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "podcast_render.html", context)

def royalti_render(request):
    if request.session.get('status') == 'Label':
        context = {
            'status': request.session.get('status'),
            'nama': request.session.get('nama'),
            'last_login': request.COOKIES['last_login'],
        }
        return render(request, "royalti_render_label.html", context)
    else:
        context = {
            'status': request.session.get('status'),
            'nama': request.session.get('nama'),
            'last_login': request.COOKIES['last_login'],
        }

        return render(request, "royalti_render.html", context)

def r_album(request):
    if request.session.get('status') == 'Songwriter':
        string = f"""
        SELECT DISTINCT a.judul as judul_album, l.nama as label_album, a.jumlah_lagu as jumlah_lagu, a.total_durasi as total_durasi, a.id as id_album, a.id_label as id_label
        FROM album AS a
        JOIN song AS s ON a.id = s.id_album
        JOIN songwriter_write_song AS sws ON s.id_konten = sws.id_song
        JOIN songwriter AS sw ON sws.id_songwriter = sw.id
        JOIN konten AS k ON s.id_konten = k.id
        JOIN LABEL as l on a.id_label = l.id
        JOIN artist as ar on s.id_artist = ar.id
        WHERE sw.id = '{request.session.get('id')}';
        """
        hasil = query(string)
        return JsonResponse(hasil, safe=False)
    elif request.session.get('status') == 'Artist':
        string = f"""
        SELECT DISTINCT a.judul as judul_album, l.nama as label_album, a.jumlah_lagu as jumlah_lagu, a.total_durasi as total_durasi, a.id as id_album, a.id_label as id_label
        FROM album AS a
        JOIN song AS s ON a.id = s.id_album
        JOIN songwriter_write_song AS sws ON s.id_konten = sws.id_song
        JOIN songwriter AS sw ON sws.id_songwriter = sw.id
        JOIN konten AS k ON s.id_konten = k.id
        JOIN LABEL as l on a.id_label = l.id
        JOIN artist as ar on s.id_artist = ar.id
        WHERE ar.id = '{request.session.get('id')}';
        """
        hasil = query(string)
        return JsonResponse(hasil, safe=False)

def r_podcast(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("podcast").select("*, konten(judul, durasi), episode(*)").execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def c_album(request):
    return None

def d_album(request, id_album):
    if request.method == 'GET':   
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        supabase = create_client(url, key)
        
        # Delete the record with the specified id_album and let cascading delete handle associated records
        response = supabase.table('album').delete().eq('id', id_album).execute()
        
        return HttpResponse(b"CREATED", status=201)
    
    return HttpResponseNotFound()

    
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
    if request.session.get('status') == 'Songwriter':
        string = f"""
        SELECT a.judul as judul_album, sw.email_akun as email_songwriter, k.judul as judul_lagu, s.total_download, s.total_play, ar.email_akun as email_artist
        FROM album AS a
        JOIN song AS s ON a.id = s.id_album
        JOIN songwriter_write_song AS sws ON s.id_konten = sws.id_song
        JOIN songwriter AS sw ON sws.id_songwriter = sw.id
        JOIN konten AS k ON s.id_konten = k.id
        JOIN artist as ar on s.id_artist = ar.id
        WHERE a.id = '{id_album}'
        AND sw.id = '{request.session.get('id')}';
        """
        hasil = query(string)
        return JsonResponse(hasil, safe=False)
    elif request.session.get('status') == 'Artist':
        string = f"""
        SELECT a.judul as judul_album, sw.email_akun as email_songwriter, k.judul as judul_lagu, s.total_download, s.total_play, ar.email_akun as email_artist
        FROM album AS a
        JOIN song AS s ON a.id = s.id_album
        JOIN songwriter_write_song AS sws ON s.id_konten = sws.id_song
        JOIN songwriter AS sw ON sws.id_songwriter = sw.id
        JOIN konten AS k ON s.id_konten = k.id
        JOIN artist as ar on s.id_artist = ar.id
        WHERE a.id = '{id_album}'
        AND ar.id = '{request.session.get('id')}';
        """
        hasil = query(string)
        return JsonResponse(hasil, safe=False)   

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
    if request.session.get('status') == 'Songwriter':
        string = f"""
        SELECT k.judul as judul_lagu, 
            a.judul as judul_album, 
            s.total_play as total_play, 
            s.total_download as total_download, 
            r.jumlah as jumlah, 
            phc.rate_royalti as rate_royalti,
            phc.rate_royalti * s.total_play as total_royalti
        FROM royalti as r
        JOIN song as s ON r.id_song = s.id_konten
        JOIN konten as k ON s.id_konten = k.id
        JOIN album as a ON s.id_album = a.id
        JOIN songwriter_write_song as sws ON s.id_konten = sws.id_song
        JOIN songwriter as so ON sws.id_songwriter = so.id
        JOIN pemilik_hak_cipta as phc ON so.id_pemilik_hak_cipta = phc.id
        WHERE so.id = '{request.session.get('id')}'
        """
        hasil = query(string)
        return JsonResponse(hasil, safe=False)
    elif request.session.get('status') == 'Artist':
        string = f"""
        SELECT k.judul as judul_lagu, 
            a.judul as judul_album, 
            s.total_play as total_play, 
            s.total_download as total_download, 
            r.jumlah as jumlah, 
            phc.rate_royalti as rate_royalti,
            phc.rate_royalti * s.total_play as total_royalti
        FROM royalti as r
        JOIN song as s ON r.id_song = s.id_konten
        JOIN konten as k ON s.id_konten = k.id
        JOIN album as a ON s.id_album = a.id
        JOIN songwriter_write_song as sws ON s.id_konten = sws.id_song
        JOIN songwriter as so ON sws.id_songwriter = so.id
        JOIN artist as ar on s.id_artist = ar.id
        JOIN pemilik_hak_cipta as phc ON ar.id_pemilik_hak_cipta = phc.id
        WHERE ar.id = '{request.session.get('id')}'
        """
        hasil = query(string)
        return JsonResponse(hasil, safe=False)

def fetch_labels(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("label").select("nama, id").execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def fetch_genres(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    # Execute the query to get all genre values
    all_genres = supabase.table("genre").select("genre").execute()
    
    # Extract the unique genre values using a set to eliminate duplicates
    unique_genres_set = {item['genre'] for item in all_genres.data}
    unique_genres_list = list(unique_genres_set)
    
    # Convert the list to JSON response
    return JsonResponse(unique_genres_list, safe=False)

def fetch_podcasters(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    # Execute the query to get all genre values
    all_podcasters = supabase.table("podcaster").select("email").execute()
    
    # Extract the unique genre values using a set to eliminate duplicates
    unique_podcasters_set = {item['email'] for item in all_podcasters.data}
    unique_podcasters_list = list(unique_podcasters_set)
    
    # Convert the list to JSON response
    return JsonResponse(unique_podcasters_list, safe=False)

def fetch_episodes(request, id_konten):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    test = supabase.table("podcast").select("*, konten(judul, durasi), episode(*)").eq('id_konten', id_konten).execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def fetch_songwriters(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)

    if request.session.get('status') == 'Songwriter':
        email = request.session.get('email')
        testing = [{'id': request.session.get('id'),
                    'email_akun': email}]
        # Return the email as a JSON response
        return JsonResponse(testing, safe=False) 
    elif request.session.get('status') == 'Artist':
        all_songwriters = supabase.from_('songwriter').select('id, email_akun').execute()
        return JsonResponse(all_songwriters.data, safe=False)

def fetch_artists(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    if request.session.get('status') == 'Songwriter':
        # Execute the query to get all genre values
        all_artists = supabase.table("artist").select("id, email_akun").execute()
        all_artists_data = all_artists.data
        # Convert the list to JSON response
        return JsonResponse(all_artists_data, safe=False)
    elif request.session.get('status') == 'Artist':
        email = request.session.get('email')
        testing = [{'id': request.session.get('id'),
                    'email_akun': email}]
        # Return the email as a JSON response
        return JsonResponse(testing, safe=False) 


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

@csrf_exempt
def add_album_ajax(request):
    if request.method == 'POST':
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        supabase = create_client(url, key)
        
        judul_album = request.POST.get("judul_album")
        id_label = request.POST.get("id_label")
        judul_lagu = request.POST.get("judul_lagu")
        artist_album = request.POST.get("artist")
        songwriter_album = request.POST.get("songwriter")
        genre_album = request.POST.get("genre")
        durasi_album = request.POST.get("total_durasi")

        # Generate UUID as a string
        uuid_lagu = str(uuid.uuid4())
        uuid_album = str(uuid.uuid4())

        # Insert data into the database
        data = supabase.table("album").insert({
            "id": uuid_album,
            "judul": judul_album,
            "jumlah_lagu": 1,
            "id_label": id_label,
            "total_durasi": durasi_album,
        }).execute()

        konten = supabase.table("konten").insert({
            "id": uuid_lagu,
            "judul": judul_lagu,
            "tanggal_rilis": datetime.datetime.now().strftime("%Y-%m-%d"),
            "tahun": 2024,
            "durasi": durasi_album,
        }).execute()

        genre_lagu = supabase.table("genre").insert({
            "id_konten": uuid_lagu,
            "genre": genre_album,
        }).execute()

        song_lagu = supabase.table("song").insert({
            "id_konten": uuid_lagu,
            "id_artist": artist_album,
            "id_album": uuid_album,
            "total_play": 0,
            "total_download": 0,
        }).execute()


        songwriter_write_song = supabase.table("songwriter_write_song").insert({
            "id_songwriter": songwriter_album,
            "id_song": uuid_lagu
        }).execute()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

@csrf_exempt
def add_song_ajax(request):
    if request.method == 'POST':
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        supabase = create_client(url, key)
        
        id_album = request.POST.get("id_album")
        id_label = request.POST.get("id_label")
        judul_lagu = request.POST.get("judul_lagu")
        artist_album = request.POST.get("artist")
        songwriter_album = request.POST.get("songwriter")
        genre_album = request.POST.get("genre")
        durasi_album = request.POST.get("total_durasi")

        # Generate UUID as a string
        uuid_lagu = str(uuid.uuid4())

        konten = supabase.table("konten").insert({
            "id": uuid_lagu,
            "judul": judul_lagu,
            "tanggal_rilis": datetime.datetime.now().strftime("%Y-%m-%d"),
            "tahun": 2024,
            "durasi": durasi_album,
        }).execute()

        genre_lagu = supabase.table("genre").insert({
            "id_konten": uuid_lagu,
            "genre": genre_album,
        }).execute()

        song_lagu = supabase.table("song").insert({
            "id_konten": uuid_lagu,
            "id_artist": artist_album,
            "id_album": id_album,
            "total_play": 0,
            "total_download": 0,
        }).execute()


        songwriter_write_song = supabase.table("songwriter_write_song").insert({
            "id_songwriter": songwriter_album,
            "id_song": uuid_lagu
        }).execute()

        selected_album = supabase.table("album").select("*").eq('id', id_album).execute()
        jumlah_sekarang = selected_album.data[0]['jumlah_lagu'] + 1
        durasi_sekarang = selected_album.data[0]['total_durasi'] + int(durasi_album)
        string = f"UPDATE album SET jumlah_lagu = {jumlah_sekarang}, total_durasi = {durasi_sekarang} WHERE id = '{id_album}';"
        hasil = query(string)

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

