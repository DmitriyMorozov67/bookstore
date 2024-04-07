from django.db import models
from django.contrib.auth.models import User
from catalog.models import Category

def image_directory_path(instance: "ImageBook", filename: str) -> str:
    return 'accounts/profile_{pk}/avatar/{filename}'.format(
        pk=instance.book.pk,
        filename=filename
    )


class Book(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='books')
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    published_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ImageBook(models.Model):
    name = models.CharField(max_length=200, null=False, blank=True)
    book = models.ForeignKey(Book, related_name='images',
                             on_delete=models.CASCADE,
                             verbose_name='book')
    image = models.ImageField(upload_to=image_directory_path)

    class Meta:
        verbose_name = 'Book image'
        verbose_name_plural = 'Book images'
        ordering = ['pk', ]

    def src(self):
        return self.image

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

