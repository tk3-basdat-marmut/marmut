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
import os
from supabase import create_client, Client


def show_main(request):
    context = {
        'name': request.session.get('name'),
        'email': request.session.get('email'),
        'password': request.session.get('password'),
        'tanggal_lahir': request.session.get('tanggal_lahir'),
        'tempat_lahir': request.session.get('tempat_lahir'),
        'gender': request.session.get('gender'),
        'is_verified': request.session.get('is_verified'),
        'kota_asal': request.session.get('kota_asal'),
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "main.html", context)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_xuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)



def login_user(request):
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    supabase = create_client(url, key)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        result = supabase.from_('akun').select('*').eq('email', username).execute()
        data = result.data
        if data == []:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
        elif data[0]['password'] == password:
            request.session['email'] = data[0]['email']
            request.session['password'] = data[0]['password']
            request.session['nama'] = data[0]['nama']
            request.session['gender'] = data[0]['gender']
            request.session['tempat_lahir'] = data[0]['tempat_lahir']
            request.session['tanggal_lahir'] = data[0]['tanggal_lahir']
            request.session['is_verified'] = data[0]['is_verified']
            request.session['kota_asal'] = data[0]['kota_asal']
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    context = {}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    request.session.flush()
    return response
