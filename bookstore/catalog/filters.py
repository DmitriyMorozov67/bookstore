from django_filters import rest_framework as filters
from store.models import Book


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Book
        fields = ['title']