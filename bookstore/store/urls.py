from django.urls import path
from .views import BookDetail, CreateComment, NewBooksFeed


urlpatterns = [
    path('api/book/<int:pk>', BookDetail.as_view(), name='book_detail'),
    path('api/book/<int:pk>/comment', CreateComment.as_view(), name='book_comment'),
    path('api/new-books-feed/', NewBooksFeed.as_view(), name='news-books-feeds'),
]