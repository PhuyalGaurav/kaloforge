from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    pass


class ResumeData(models.Model):
    image = models.URLField(max_length=2000)  # Increased from 1000
    name = models.CharField(max_length=1001)
    email = models.EmailField(max_length=2001)
    phone = models.CharField(max_length=2002)
    summary = models.TextField(max_length=2003)
    skills = models.TextField(max_length=2004)
    education = models.TextField(max_length=2005)
    experience = models.TextField(max_length=2006)
    projects = models.TextField(max_length=2007)
    certifications = models.TextField(max_length=2008)
    languages = models.TextField(max_length=2009)
    interests = models.TextField(max_length=2010)
    created_at = models.DateTimeField(auto_now_add=True)
    template = models.CharField(max_length=2000)  # Increased from 1003

    def __str__(self):
        return f"{self.name} - {self.created_at}"


class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.OneToOneField(ResumeData, on_delete=models.CASCADE)
    template_used = models.CharField(max_length=2000)  # Increased from 200
    html_template = models.TextField()
    pdf_link = models.URLField(max_length=2000)  # Increased from 400
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def pdf_url(self):
        if hasattr(self, "pdf") and self.pdf:
            return self.pdf.url
        return None

    def __str__(self):
        return f"{self.user.username} - {self.data.name}- {self.created_at}"
