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
    test = supabase.table("chart_songs").select("*").eq('id', id).execute()
    response = test.data
    # Convert dictionary to JSON response
    return JsonResponse(response, safe=False)

def chart_detail(request):
    return render(request, "chart_detail.html")