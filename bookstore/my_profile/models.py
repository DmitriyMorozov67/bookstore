from django.db import models
from django.contrib.auth.models import User
from store.models import Book


def avatar_directory_path(instance: "Avatar", filename: str) -> str:
    return 'accounts/profile_{pk}/avatar/{filename}'.format(
        pk=instance.profile.pk,
        filename=filename
    )


class Avatar(models.Model):
    profile = models.OneToOneField('Profile', verbose_name='avatar',
                                   on_delete=models.CASCADE)
    image = models.ImageField(upload_to=avatar_directory_path)

    class Meta:
        verbose_name = 'Profile image'
        verbose_name_plural = 'Profile images'
        ordering = ['pk', ]

    def src(self):
        return f'/media/{self.image}'

    def alt(self):
        return f'{self.profile.user.username}_avatar'

    def __str__(self):
        return f'{self.profile.user.username}_avatar'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=False, blank=True, default='')
    last_name = models.CharField(max_length=100, null=False, blank=True, default='')
    email = models.EmailField(max_length=150)
    favorite_books = models.ManyToManyField(Book, related_name="favorited_by")

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['pk', ]

    def __str__(self):
        return self.user.username

