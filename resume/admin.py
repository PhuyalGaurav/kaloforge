from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ResumeData, Resume


class ResumeDataAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "created_at")
    search_fields = ("name", "email", "phone")
    list_filter = ("created_at",)


class ResumeAdmin(admin.ModelAdmin):
    list_display = ("user", "template_used", "created_at")
    search_fields = ("user", "template_used")
    list_filter = ("created_at",)


admin.site.register(ResumeData, ResumeDataAdmin)
admin.site.register(Resume, ResumeAdmin)

admin.site.register(User, UserAdmin)
