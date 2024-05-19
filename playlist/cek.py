import os
import asyncio
from supabase import create_client
SUPABASE_URL="https://kjbsshuatchylgygwyzo.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtqYnNzaHVhdGNoeWxneWd3eXpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTQwMzc4MDgsImV4cCI6MjAyOTYxMzgwOH0.Lkrzi9awrcAOKgIcWqflMEJNFg-4Bohd4ckO31GPm1E"
url = SUPABASE_URL
key = SUPABASE_KEY
import os
from supabase import create_client

supabase = create_client(url, key)

def check_column_names():
    playlist_song_data = supabase.table("playlist_song").select("*").execute()
    column_names = list(playlist_song_data.data[0].keys())
    print(column_names)

if __name__ == "__main__":
    check_column_names()