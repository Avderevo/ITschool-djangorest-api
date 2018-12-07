from django.contrib import admin
from .models import Course, Lesson, Message


@admin.register(Course, Lesson, Message)
class StudyAdmin(admin.ModelAdmin):
    pass