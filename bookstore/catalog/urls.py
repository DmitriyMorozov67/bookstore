from django.urls import path
from .views import Catalog, CategoriesList


urlpatterns = [
    path('api/catalog', Catalog.as_view(), name='books-list'),
    path('api/catalog/<int:pk>/', Catalog.as_view(), name='book-catalog-detail'),
    path('api/categories', CategoriesList.as_view(), name='categories')
]