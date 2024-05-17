from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from supabase import create_client
from postgrest.exceptions import APIError
import os
import uuid


# Setup Supabase client
def get_supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("Supabase URL or Key is not set in environment variables")
    return create_client(url, key)


def r_list_packages(request):
    supabase = get_supabase_client()
    response = supabase.table("paket").select("*").execute()
    packages = response.data
    context = {
        'packages': packages,
        'user_email': request.session.get('email'),  # Menambahkan email pengguna dari sesi
        'is_premium': request.session.get('is_premium')  # Misal status premium/non-premium
    }
    return render(request, 'subscribe.html', context)


def c_subscribe_to_package(request):
    if request.method == "POST":
        supabase = get_supabase_client()
        email = request.POST.get("email")
        jenis_paket = request.POST.get("jenis_paket")
        timestamp_dimulai = request.POST.get("timestamp_dimulai")
        timestamp_berakhir = request.POST.get("timestamp_berakhir")
        metode_bayar = request.POST.get("metode_bayar")
        nominal = request.POST.get("nominal")

        # Generate transaction_id using uuid
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
        supabase.table("transaction").insert(transaction).execute()
        return HttpResponse("Subscription successful", status=201)
    return HttpResponse("Invalid request", status=400)


def r_transaction_history(request, email):
    supabase = get_supabase_client()
    response = supabase.table("transaction").select("*").eq("email", email).order("timestamp_dimulai", desc=True).execute()
    history = response.data
    return render(request, "history.html", {'transactions': history})


def search_content(request):
    query = request.GET.get('q', '')
    supabase = get_supabase_client()
    try:
        # Search for songs
        songs = supabase.table("song").select("*").ilike('judul', f'%{query}%').execute().data
        
        # Search for podcasts and user playlists (assuming the tables and columns exist)
        podcasts = supabase.table("podcast").select("*").ilike('judul', f'%{query}%').execute().data
        user_playlists = supabase.table("user_playlist").select("*").ilike('judul', f'%{query}%').execute().data
        
        results = {
            'songs': songs,
            'podcasts': podcasts,
            'user_playlists': user_playlists
        }
        # If no results found, display a message
        if not (songs or podcasts or user_playlists):
            return render(request, 'search.html', {'message': 'No results found for your search.'})
        
        return render(request, 'search_results.html', {'results': results, 'query': query})
    except APIError as e:
        error_message = str(e)
        return render(request, 'search.html', {'message': f'An error occurred: {error_message}'})


def r_downloaded_songs(request):
    supabase = get_supabase_client()
    email = request.session.get('email')  # Assuming email is stored in session
    response = supabase.table("downloaded_song").select("*, song(*)").eq("email_downloader", email).execute()
    return render(request, "downloaded_songs.html", {'songs': response.data})


def song_detail(request, id_song):
    supabase = get_supabase_client()
    response = supabase.table("song").select("*").eq("id_konten", id_song).execute()
    song_details = response.data[0] if response.data else None
    return render(request, "song_detail.html", {'song': song_details})


# def d_downloaded_songs(request, id_song):
#     if request.method == "POST":
#         supabase = get_supabase_client()
#         email = request.user.email
#         supabase.table("downloaded_song").delete().match({"id_song": id_song, "email_downloader": email}).execute()
#         return redirect('r-downloaded-songs')
#     return HttpResponse("Method not allowed", status=405)

def d_downloaded_songs(request, id_song):
    if request.method == "POST":
        supabase = get_supabase_client()
        email = request.session.get('email')  # Assuming email is stored in session
        
        # Delete the downloaded song from the database
        supabase.table("downloaded_song").delete().match({"id_song": id_song, "email_downloader": email}).execute()
        
        # Redirect to deletion_success.html with a success message
        message = "Lagu berhasil dihapus dari daftar unduhan."
        return render(request, 'deletion_success.html', {'message': message})
    
    return HttpResponse("Method not allowed", status=405)

def payment(request, jenis_paket, harga):
    package = {
        'jenis': jenis_paket,
        'harga': harga
    }
    return render(request, 'payment.html', {'package': package})
