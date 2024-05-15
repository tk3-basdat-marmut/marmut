from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from supabase import create_client
import os
import uuid


# Setup Supabase client
def get_supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    return create_client(url, key)


def r_list_packages(request):
    supabase = get_supabase_client()
    response = supabase.table("PAKET").select("*").execute()
    packages = response.data
    return JsonResponse(packages, safe=False)


def c_subscribe_to_package(request):
    if request.method == "POST":
        supabase = get_supabase_client()
        email = request.POST.get("email")
        jenis_paket = request.POST.get("jenis_paket")
        timestamp_dimulai = request.POST.get("timestamp_dimulai")
        timestamp_berakhir = request.POST.get("timestamp_berakhir")
        metode_bayar = request.POST.get("metode_bayar")
        nominal = request.POST.get("nominal")
        transaction_id = str(uuid.uuid4())
        transaction = {
            "id": transaction_id,
            "jenis_paket": jenis_paket,
            "email": email,
            "timestamp_dimulai": timestamp_dimulai,
            "timestamp_berakhir": timestamp_berakhir,
            "metode_bayar": metode_bayar,
            "nominal": nominal
        }
        supabase.table("TRANSACTION").insert(transaction).execute()
        return HttpResponse("Subscription successful", status=201)
    return HttpResponse("Invalid request", status=400)


def r_transaction_history(request, email):
    supabase = get_supabase_client()
    response = supabase.table("TRANSACTION").select("*").eq("email", email).order("timestamp_dimulai", desc=True).execute()
    history = response.data
    return JsonResponse(history, safe=False)


def search_content(request):
    query = request.GET.get('q', '')
    supabase = get_supabase_client()
    # Search for songs, podcasts, and user playlists
    songs = supabase.table("SONG").select("*, ARTIST(*)").ilike('judul', f'%{query}%').execute().data
    podcasts = supabase.table("PODCAST").select("*, PODCASTER(*)").ilike('judul', f'%{query}%').execute().data
    user_playlists = supabase.table("USER_PLAYLIST").select("*, AKUN(email)").ilike('judul', f'%{query}%').execute().data

    results = {
        'songs': songs,
        'podcasts': podcasts,
        'user_playlists': user_playlists
    }
    # If no results found, display a message
    if not (songs or podcasts or user_playlists):
        return render(request, 'search.html', {'message': 'No results found for your search.'})

    return render(request, 'search_results.html', {'results': results, 'query': query})


def r_downloaded_songs(request):
    supabase = get_supabase_client()
    email = request.user.email  # Assuming authentication
    response = supabase.table("DOWNLOADED_SONG").select("*, SONG(*)").eq("email_downloader", email).execute()
    return render(request, "downloaded_songs.html", {'songs': response.data})


def song_detail(request, id_song):
    supabase = get_supabase_client()
    response = supabase.table("SONG").select("*").eq("id_konten", id_song).execute()
    song_details = response.data[0] if response.data else None
    return render(request, "song_detail.html", {'song': song_details})


def d_downloaded_songs(request, id_song):
    if request.method == "POST":
        supabase = get_supabase_client()
        email = request.user.email
        supabase.table("DOWNLOADED_SONG").delete().match({"id_song": id_song, "email_downloader": email}).execute()
        return redirect('r-downloaded-songs')
    return HttpResponse("Method not allowed", status=405)
