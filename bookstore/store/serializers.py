import datetime

from rest_framework import serializers
from .models import Book, ImageBook, Comment


class ImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()
    alt = serializers.CharField(default='images')

    class Meta:
        model = ImageBook
        fields = ['src', 'alt']

    def get_src(self, obj):
        if obj.image:
            return obj.image.url
        return None


class CommentSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['author', 'book', 'text', 'date']

    def get_date(self, instance):
        date = instance.date + datetime.timedelta(hours=3)
        return datetime.datetime.strftime(date, '%d.%m.%Y %H:%M')


class BookSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    comment = CommentSerializer(many=True, required=False)

    class Meta:
        model = Book
        fields = ['pk', 'category', 'title', 'author',
                  'description', 'created_at',
                  'published_date', 'comment',
                  'images', 'created_at']


class BookCatalogSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True, required=False)
    comment = CommentSerializer(many=True, required=False)

    class Meta:
        model = Book
        fields = ['pk', 'category', 'title', 'author',
                  'description', 'created_at',
                  'published_date', 'comment',
                  'image', 'created_at']


