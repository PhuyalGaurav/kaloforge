from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import User
from .utils import generate_data, generate_pdf_template_1
import json


def index(request):
    return render(request, "resume/getstarted.html")


def home(request):
    return render(request, 'resume/home.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))  
        else:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "resume/login.html")  
    else:
        return render(request, "resume/login.html")

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            messages.error(request, "Passwords must match.")
            return render(request, "resume/signup.html")
        
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address.")
            return render(request, "resume/signup.html")
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "resume/signup.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "resume/signup.html")

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)  
            return HttpResponseRedirect(reverse("home"))
        except IntegrityError:
            messages.error(request, "An error occurred. Please try again.")
            return render(request, "resume/signup.html")

    else:
        return render(request, "resume/signup.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))
    return render(request, "resume/home.html")


# Testing purposes ko lagi matrai ho hai yo error ayo bhane comment garde yo function
def generate_resume(request):
    data = generate_data(
        "Name: Gaurav Phuyal, Email:phuyalgaurav90@gmail.com, Experienced python developer with over 30 years of experience, Skills: Python, Django, Flask, FastAPI, JavaScript, React, Angular, Vue, HTML, CSS, SQL, NoSQL, Docker, Kubernetes, AWS, Azure, GCP, Git, CI/CD, Agile, Scrum, Kanban, TDD, BDD, DDD, Microservices, REST, GraphQL, etc..."
    )

    generate_pdf_template_1(json.loads(data))
    return render(request, "resume/home.html")
