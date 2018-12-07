from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Activation, Statistic


@admin.register(Profile, Activation, Statistic)
class UserAdmin(admin.ModelAdmin):
    pass