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

def r_chart(request):
    return render(request, "chart.html")

def chart_detail(request):
    return render(request, "chart_detail.html")