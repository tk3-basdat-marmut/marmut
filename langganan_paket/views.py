from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from supabase import create_client, Client
import os
import uuid
import datetime


# Initialize Supabase client
def init_supabase():
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY')
    if not url or not key:
        raise ValueError("Supabase URL and Key must be set in the environment.")
    return create_client(url, key)


@csrf_exempt
@login_required
def subscribe_package(request):
    if request.method == "POST":
        email = request.user.email
        jenis_paket = request.POST.get("jenis_paket")
        metode_bayar = request.POST.get("metode_bayar")
        nominal = int(request.POST.get("nominal"))
        
        supabase = init_supabase()
        # Generate UUID for transaction ID
        transaction_id = str(uuid.uuid4())
        # Current timestamp
        timestamp_now = datetime.datetime.now()
        # Subscription validity (e.g., one month)
        timestamp_end = timestamp_now + datetime.timedelta(days=30)

        try:
            # Insert transaction into TRANSACTION table
            transaction_response = supabase.table("TRANSACTION").insert({
                "id": transaction_id,
                "jenis_paket": jenis_paket,
                "email": email,
                "timestamp_dimulai": timestamp_now,
                "timestamp_berakhir": timestamp_end,
                "metode_bayar": metode_bayar,
                "nominal": nominal,
            }).execute()

            # Check and insert into PREMIUM if not already a member
            premium_check = supabase.table("PREMIUM").select("*").eq("email", email).execute()
            if premium_check.data == []:
                supabase.table("PREMIUM").insert({"email": email}).execute()

            return HttpResponseRedirect(reverse('subscription_success'))
        except Exception as e:
            # Log this error to a logging system ideally
            return HttpResponseNotFound('An error occurred during the subscription process.')

    else:
        # Fetch available packages
        supabase = init_supabase()
        packages = supabase.table("PAKET").select("*").execute().data
        return render(request, 'subscribe.html', {'packages': packages})


@login_required
def transaction_history(request):
    email = request.user.email
    supabase = init_supabase()
    transactions = supabase.table("TRANSACTION").select("*").eq("email", email).order("timestamp_dimulai", desc=True).execute().data
    return render(request, 'payment.html', {'transactions': transactions})


def subscription_success(request):
    return render(request, 'history.html')


@login_required
def search(request):
    query = request.GET.get('query', '')
    supabase = init_supabase()

    if query:
        songs = supabase.table("SONG").select("*, artist:ARTIST (*)").ilike("judul", f"%{query}%").execute().data
        podcasts = supabase.table("PODCAST").select("*, podcaster:PODCASTER (*)").ilike("judul", f"%{query}%").execute().data
        user_playlists = supabase.table("USER_PLAYLIST").select("*, creator:AKUN (*)").ilike("judul", f"%{query}%").execute().data
        
        results = {
            'songs': songs,
            'podcasts': podcasts,
            'user_playlists': user_playlists
        }
    else:
        results = {}

    return render(request, 'search.html', {'query': query, 'results': results})


@login_required
def downloaded_songs(request):
    supabase = init_supabase()
    email = request.user.email
    # Fetch songs that have been downloaded by the user
    downloaded_songs = supabase.table("DOWNLOADED_SONG").select("*, song:SONG (*)").eq("email_downloader", email).execute().data
    
    # For additional details like artist name, you might need to make additional queries or adjust your database structure for easier access
    songs_with_details = []
    for entry in downloaded_songs:
        song_id = entry['song']['id_konten']
        artist_details = supabase.table("ARTIST").select("*").eq("id", entry['song']['id_artist']).execute().data
        entry['artist_name'] = artist_details[0]['name'] if artist_details else "Unknown Artist"
        songs_with_details.append(entry)

    return render(request, 'downloaded_songs.html', {'songs': songs_with_details})


@login_required
@csrf_exempt
def delete_downloaded_song(request, song_id):
    if request.method == 'POST':
        supabase = init_supabase()
        email = request.user.email
        song_title = request.POST.get('song_title')

        # Delete the song from downloaded list
        delete_response = supabase.table("DOWNLOADED_SONG").delete().match({"id_song": song_id, "email_downloader": email}).execute()
        
        if delete_response.status_code == 200:
            # Decrement the total_download counter
            supabase.table("SONG").update({"total_download": supabase.raw("total_download - 1")}).eq("id_konten", song_id).execute()
            message = f"Berhasil menghapus Lagu dengan judul ‘{song_title}’ dari daftar unduhan!"
            return render(request, 'deletion_success.html', {'message': message})
        else:
            return HttpResponseNotFound('Failed to delete the song.')

    return HttpResponseNotAllowed(['POST'])
