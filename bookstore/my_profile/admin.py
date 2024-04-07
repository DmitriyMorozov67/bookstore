from django.contrib import admin
from .models import Profile, Avatar


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['pk', 'first_name', 'last_name', 'user']
    list_display_links = ['pk', 'first_name']
    ordering = ['pk', ]


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ['pk', '__str__']
    list_display_links = ['pk', ]
    ordering = ['pk', ]
