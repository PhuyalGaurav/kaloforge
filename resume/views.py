from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings

def index(request):
    return render(request, 'resume/getstarted.html')

def home(request):
    return render(request, 'resume/home.html')