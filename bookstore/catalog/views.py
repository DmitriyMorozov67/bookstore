
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend


from .models import Category
from .serializers import CategorySerializer
from .filters import BookFilter

from store.models import Book
from store.serializers import BookCatalogSerializer


class Catalog(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def get(self, request: Request, pk=None):
        if pk:
            book = self.get_object(pk)
            serializer = BookCatalogSerializer(book)
        else:
            books = Book.objects.all()
            serializer = BookCatalogSerializer(books, many=True)
        return Response(serializer.data)

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            return Response({'error': 'Такой книги не существует'}, status=status.HTTP_404_NOT_FOUND)


class CategoriesList(APIView):
    def get(self, request: Request):
        categories = Category.objects.filter(parent=None)
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data)
