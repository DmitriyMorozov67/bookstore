from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Avatar
from store.serializers import BookSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['src', 'alt']


class ProfileSerializer(serializers.ModelSerializer):
    avatar = AvatarSerializer(many=False, required=False)
    favorite_books = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'avatar', 'favorite_books']

    def get_favorite_books(self, obj):
        favorite_books = obj.favorite_books.all()
        return BookSerializer(favorite_books, many=True).data


class PasswordChangeSerializer(serializers.ModelSerializer):
    passwordCurrent = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    passwordReply = serializers.CharField(required=True)