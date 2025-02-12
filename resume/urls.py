from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("home", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout_view, name="logout"),
    path("form", views.form, name="form"),
    path("resume", views.resume, name="resume"),
    path("api/resume/<int:resume_id>/", views.resume_api, name="resume_api"),
    path("generated/<int:resume_id>/", views.generated_view, name="generated"),
]
