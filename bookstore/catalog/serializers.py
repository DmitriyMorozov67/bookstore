from rest_framework import serializers
from .models import Category


class SubSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Category
        fields = ['id', 'title', 'image']

    def get_image(self, obj):
        return {
            'src': obj.image.url,
            'alt': 'pictures',
        }


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubSerializer(many=True, required=False)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'subcategories']

    def get_image(self, obj):
        return {
            'src': obj.image.url,
            'alt': 'pictures',
        }