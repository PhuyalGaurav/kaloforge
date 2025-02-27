from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import User, ResumeData, Resume
from .utils import generate_data, generate_html_template_1, generate_pdf_from_html
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect


def index(request):
    return render(request, "resume/getstarted.html")


@login_required(login_url="/login")
def resume_api(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id, user=request.user)
        return JsonResponse(
            {
                "id": resume.id,
                "data": {
                    "name": resume.data.name if resume.data else "",
                },
                "pdf_url": resume.pdf_link,  # Use pdf_link here
                "created_at": resume.created_at.isoformat(),
                "updated_at": (
                    resume.updated_at.isoformat()
                    if hasattr(resume, "updated_at")
                    else None
                ),
            }
        )
    except Resume.DoesNotExist:
        return JsonResponse({"error": "Resume not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@login_required(login_url="/login")
def generated_view(request, resume_id):
    try:
        # Get resume only if it belongs to the current user
        resume = Resume.objects.get(id=resume_id, user=request.user)
        context = {
            "resume": resume,
            "pdf_url": resume.pdf_link,
            "html_template": resume.html_template,
        }
        return render(request, "resume/generated.html", context)
    except Resume.DoesNotExist:
        messages.error(request, "Resume not found or access denied.")
        return redirect("home")


@login_required(login_url="/login")
def resume(request):
    # Only get resumes for the logged-in user
    resumes = Resume.objects.filter(user=request.user).order_by("-created_at")
    active_resume = resumes.first() if resumes.exists() else None

    return render(
        request,
        "resume/resume.html",
        {
            "resumes": resumes,
            "active_resume": active_resume,
            "debug": settings.DEBUG,
        },
    )


def home(request):
    if request.user.is_authenticated:
        resumes = Resume.objects.filter(user=request.user).order_by("-created_at")
        return render(request, "resume/home.html", {"resume": resumes})
    return render(request, "resume/home.html")


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            remember_me = request.POST.get("rememberMe", None)

            if remember_me is not None:
                request.session.set_expiry(15552000)
            else:
                request.session.set_expiry(0)

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
        remember_me = request.POST.get("rememberMe", None)

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
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            user.save()
            login(request, user)
            if remember_me is not None:
                request.session.set_expiry(15552000)
            else:
                request.session.set_expiry(0)

            return HttpResponseRedirect(reverse("home"))
        except IntegrityError:
            messages.error(request, "An error occurred. Please try again.")
            return render(request, "resume/signup.html")

    else:
        return render(request, "resume/signup.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


# Testing purposes ko lagi matrai ho hai yo error ayo bhane comment garde yo function
# def generate_resume(request):
#     data = generate_data(
#         "Name: Gaurav Phuyal, Email:phuyalgaurav90@gmail.com, Experienced python developer with over 30 years of experience, Skills: Python, Django, Flask, FastAPI, JavaScript, React, Angular, Vue, HTML, CSS, SQL, NoSQL, Docker, Kubernetes, AWS, Azure, GCP, Git, CI/CD, Agile, Scrum, Kanban, TDD, BDD, DDD, Microservices, REST, GraphQL, etc..."
#     )

#     generate_pdf_template_1(json.loads(data))
#     return render(request, "generator/template1.html")


# Yo Yo Yo 1-4-8 3 to the 3 to the 6 to the 9. Representing the ABQ. What up BIATCH! Leave at the tone.
# JESSI WTF IS THIS?? WHO TF WILL FILL A FORM THAT IS THIS BIG??


@login_required(login_url="/login")
def form(request):
    if request.method == "POST":
        try:
            # Create resume data
            resume_data = ResumeData(
                name=request.POST.get("name", ""),
                email=request.POST.get("email", ""),
                phone=request.POST.get("phone", ""),
                summary=request.POST.get("summary", ""),
                skills=request.POST.get("skills", ""),
                education=request.POST.get("education", ""),
                experience=request.POST.get("experience", ""),
                projects=request.POST.get("projects", ""),
                certifications=request.POST.get("certifications", ""),
                languages=request.POST.get("languages", ""),
                interests=request.POST.get("interests", ""),
            )
            if "image" in request.FILES:
                resume_data.image=request.FILES["image"]
                
            resume_data.save()

            data = generate_data(
                f"""Name: {resume_data.name}, 
                   Email: {resume_data.email},
                   Phone: {resume_data.phone},
                   Summary: {resume_data.summary},
                   Skills: {resume_data.skills},
                   Education: {resume_data.education},
                   Experience: {resume_data.experience},
                   Projects: {resume_data.projects},
                   Certifications: {resume_data.certifications},
                   Languages: {resume_data.languages},
                   Interests: {resume_data.interests},
                """
            )

            html = generate_html_template_1(data)
            link = generate_pdf_from_html(html)

            # Create resume and assign to current user
            resume = Resume(
                user=request.user,  # Ensure the resume is linked to current user
                data=resume_data,
                template_used="template1",
                html_template=html,
                pdf_link=link,
            )
            resume.save()

            return redirect("generated", resume_id=resume.id)
        except Exception as e:
            messages.error(request, f"Error creating resume: {str(e)}")
            return render(request, "resume/form.html")

    return render(request, "resume/form.html")
