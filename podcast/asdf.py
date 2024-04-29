from dotenv import load_dotenv
load_dotenv()
from django.shortcuts import render
import os
from supabase import create_client, Client
import json

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
test = supabase.table("podcast").select("*").execute()
response = test.data
response_dicts = [item for item in response]
print(response_dicts)
