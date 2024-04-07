from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, ProfileDetail, ChangePassword, AvatarUpdatedView

app_name = 'users'

urlpatterns = [
    path('api/register', RegistrationView.as_view(), name='register'),
    path('api/login', LoginView.as_view(), name='login'),
    path('api/logout', LogoutView.as_view(), name='logout'),
    path('api/profile', ProfileDetail.as_view(), name='profile'),
    path('api/profile/favorites', ProfileDetail.as_view(), name='add-to-favorites'),
    path('api/profile/avatar', AvatarUpdatedView.as_view(), name='profile_avatar'),
    path('api/profile/password', ChangePassword.as_view(), name='profile_password'),
]