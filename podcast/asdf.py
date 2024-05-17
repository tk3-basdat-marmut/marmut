from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import render
import os
from supabase import create_client, Client
import json

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
# test = supabase.table("podcast").select("*").execute()

# response = test.data
# response_dicts = [item for item in response]
# print(response_dicts)

# def fetch_podcast_details():
#     # Call the custom query function
#     response = supabase.rpc('get_podcast_details').execute()
    
#     if response.status_code == 200:
#         print(response.data)  # Debug: Print the fetched data
#         return response.data
#     else:
#         print("Error fetching data:", response.status_code, response.error_message)
#         return []

# def fetch_podcast_details():
#     # Call the custom query function
#     response = supabase.view('podcast_list').select("*").execute()
    
#     # if response.status_code == 200:
#     return response.data
#     # else:
#     #     return []