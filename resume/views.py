from django.shortcuts import render
from django.conf import settings
from . import utils

def home(request):
    
    return render(request, 'resume/home.html')