from django.shortcuts import render
from django.http import HttpResponse

# grabbing .env variables
from django.conf import settings
host_url = settings.HOST_URL

# Create your views here.

def login(request):
    return render(request,'login.html', {'host_url': host_url})

def register(request):
    return render(request,'register.html', {'host_url': host_url})

def home(request):
    return render(request,'home.html', {'host_url': host_url})

def friends(request):
    return render(request,'friends.html', {'host_url': host_url})

def profile(request):
    return render(request,'profile.html', {'host_url': host_url})
