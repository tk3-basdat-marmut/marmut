from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import render
import os
from supabase import create_client, Client
import json
from query import query

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
test = supabase.table("song").select("*, konten(judul), album(judul), artist(email_akun)").eq('id_album', 'cf5b9a32-5fe4-4d02-b893-acc842752d69').execute()
all_genres = supabase.table("genre").select("genre").execute()

all_genres = supabase.table("songwriter").select("*, song(*)").eq('id', 'acf6d78d-10f4-4cd3-9305-05793c3c7d1f').execute()

string = """
SELECT a.judul as judul_album, sw.email_akun as email_songwriter, k.judul as judul_lagu, s.total_download, s.total_play, ar.email_akun as email_artist
FROM album AS a
JOIN song AS s ON a.id = s.id_album
JOIN songwriter_write_song AS sws ON s.id_konten = sws.id_song
JOIN songwriter AS sw ON sws.id_songwriter = sw.id
JOIN konten AS k ON s.id_konten = k.id
JOIN artist as ar on s.id_artist = ar.id
WHERE a.id = '09aae45e-7a47-4f9e-af95-b9d105437108'
AND sw.id = 'e72e019c-d0a4-4ebc-8f22-c7e4216e4b11';
"""

string1 = """
SELECT *
FROM akun as a
JOIN artist as p on p.email_akun = a.email
"""

string2 = """
SELECT k.judul as judul_lagu, a.judul as judul_album, s.total_play as total_play, s.total_download as total_download
FROM royalti as r
JOIN song as s on r.id_song = s.id_konten
JOIN konten as k on s.id_konten = k.id
JOIN album as a on s.id_album = a.id
JOIN songwriter_write_song as sws on s.id_konten = sws.id_song
JOIN songwriter as so on sws.id_songwriter = so.id
WHERE so.id = '7ec6a544-87fb-4303-b720-255b6e2f93a6'
"""

string = f"""
SELECT e.judul as judul_episode, e.deskripsi as deskripsi_episode, e.durasi as durasi_episode, e.tanggal_rilis as tanggal_rilis_episode, k.judul as judul_podcast
from episode as e
JOIN konten as k on k.id = e.id_konten_podcast
WHERE e.id_konten_podcast = 'b432597f-9a74-44d2-820c-c0b8fe1705ac'
"""

string = f"""
    SELECT a.id as album_id, k.id as konten_id, a.
    FROM album as a
    JOIN song as s on s.id_album = a.id
    JOIN konten as k on s.id_konten = k.id
    WHERE s.id_konten = '27b1decd-22b3-4a54-823d-fe00b7cf7ab3';
"""
hasil = query(string)
print(hasil)


