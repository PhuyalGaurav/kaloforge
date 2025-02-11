from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    pass


class ResumeData(models.Model):
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    summary = models.TextField()
    skills = models.TextField()
    education = models.TextField()
    experience = models.TextField()
    projects = models.TextField()
    certifications = models.TextField()
    languages = models.TextField()
    interests = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.created_at}"


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.OneToOneField(ResumeData, on_delete=models.CASCADE)
    template_used = models.CharField(max_length=100)
    html_template = models.TextField()
    pdf_link = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.pdf}"
