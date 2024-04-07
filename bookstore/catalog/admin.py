from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'image']
    list_display_links = ['pk', 'title']
    ordering = ['pk', ]