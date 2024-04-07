from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_spectacular.utils import extend_schema


from datetime import datetime

from .models import Book, Comment
from .serializers import BookSerializer, CommentSerializer


@extend_schema(tags=['book'])
class BookDetail(APIView):
    @extend_schema(
        responses={
            status.HTTP_200_OK: BookSerializer
        }
    )
    def get(self, request: Request, pk):
        book = Book.objects.get(pk=pk)
        serializer = BookSerializer(book, many=False)
        return Response(serializer.data)


class NewBooksFeed(APIView):
    def get(self, request: Request):
        new_books = Book.objects.order_by('-published_date')
        serializer = BookSerializer(new_books, many=True)
        return Response(serializer.data)


@extend_schema(tags=['book'])
@extend_schema(
    request=CommentSerializer,
    responses={
        status.HTTP_200_OK: CommentSerializer
    },
)
class CreateComment(CreateModelMixin, GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, pk):
        book = Book.objects.get(pk=pk)
        request.data['date'] = datetime.now()
        request.data['book'] = book.pk
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        Comment.objects.create(
            author=request.data['author'],
            text=request.data['text'],
            data=datetime.now(),
            book_id=book.pk,
        )

        return Response(request.data)