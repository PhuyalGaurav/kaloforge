from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from .utils import generate_data, generate_pdf_template_1
import json


def index(request):
    return render(request, "resume/getstarted.html")


def home(request):
    return render(request, "resume/home.html")


# Testing purposes ko lagi matrai ho hai yo error ayo bhane comment garde yo function
def generate_resume(request):
    data = generate_data(
        "Name: Gaurav Phuyal, Email:phuyalgaurav90@gmail.com, Experienced python developer with over 30 years of experience, Skills: Python, Django, Flask, FastAPI, JavaScript, React, Angular, Vue, HTML, CSS, SQL, NoSQL, Docker, Kubernetes, AWS, Azure, GCP, Git, CI/CD, Agile, Scrum, Kanban, TDD, BDD, DDD, Microservices, REST, GraphQL, etc..."
    )

    generate_pdf_template_1(json.loads(data))
    return render(request, "resume/home.html")
