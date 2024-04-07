from django.contrib import admin
from .models import Book, ImageBook, Comment


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['pk', 'title', 'author', 'category', 'created_at']
    list_display_links = ['pk', 'title']
    ordering = ['pk', '-created_at']


@admin.register(ImageBook)
class ImageBookAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'book']
    list_display_links = ['pk', 'book']
    ordering = ['pk']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['pk', 'author', 'date', 'book']
    list_display_links = ['pk', 'book']
    ordering = ['pk', '-date']