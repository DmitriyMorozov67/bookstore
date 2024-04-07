from rest_framework import status
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProfileSerializer, PasswordChangeSerializer
from django.contrib.auth import logout
from .models import Profile, Avatar
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from store.models import Book
import json


@extend_schema(tags=['auth'])
class RegistrationView(APIView):
    @extend_schema(
        parameters=[OpenApiParameter('name', required=True),
                    OpenApiParameter('username', required=True),
                    OpenApiParameter('password', required=True)],
        responses={
            200: OpenApiResponse(description='successful operation'),
            500: OpenApiResponse(description='unsuccessful operation')
        }
    )
    def post(self, request: Request):

        data = json.loads(list(request.data.keys())[0])
        serializer = UserSerializer(data=data)
        username = data.get('username')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Такой пользователь уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            name = data.get('name')
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            try:
                user = User.objects.create_user(username=username, password=password)
                user.first_name = name
                user.save()
                Profile.objects.create(user=user, fullName=name)
                user = authenticate(username=username, password=password)
                login(request, user)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'success': 'Регистрация прошла успешна'}, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['auth'])
class LoginView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter('username', required=True),
            OpenApiParameter('password', required=True)],
        responses={
            200: OpenApiResponse(description='successful operation'),
            500: OpenApiResponse(description='unsuccessful operation')
        }
    )
    def post(self, request):
        data = json.loads(list(request.data.keys())[0])
        print(data)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username,
                            password=password)
        if user is not None:
            login(request, user)
        else:
            return Response('Неверные учетные данные', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('Аутентификация прошла успешно', status=status.HTTP_200_OK)


@extend_schema(
    tags=['auth']
)
class LogoutView(APIView):

    @extend_schema(
        responses={
            200: OpenApiResponse(description='successful operation')
        }
    )
    def post(self, request):
        logout(request)
        return reverse_lazy('users:sign-in')


@extend_schema(tags=['profile'])
class ProfileDetail(APIView):
    @extend_schema(
        responses={
            status.HTTP_200_OK: ProfileSerializer("first_name")
        }
    )
    def get(self, request: Request):
        user = request.user.pk
        profile = Profile.objects.get(user_id=user)
        serializer = ProfileSerializer(profile, many=False)
        return Response(serializer.data)

    def post(self, request: Request):
        data = request.data
        user = request.user.pk
        profile = Profile.objects.get(user_id=user)

        profile.first_name = data.get('first_name')
        profile.last_name = data.get('last_name')
        profile.email = data.get('email')
        profile.save()

        return Response('Update successful', status=status.HTTP_200_OK)

    @extend_schema(
        request=ProfileSerializer,
        responses={
            status.HTTP_200_OK: "Book added to favorites",
            status.HTTP_404_NOT_FOUND: "Book not found",
        }
    )
    def add_to_favorites(self, request, pk=None):
        user_profile = Profile.objects.get(user=request.user)
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Книга не найдена'}, status=status.HTTP_404_NOT_FOUND)

        user_profile.favorite_books.add(book)
        return Response({'status': 'Книга добавлена в избранное'}, status=status.HTTP_200_OK)


class AvatarUpdatedView(APIView):
    def post(self, request: Request):
        new_avatar = request.data.get('avatar')
        user = request.user.pk
        profile = Profile.objects.get(user_id=user)
        avatar, created = Avatar.objects.get_or_create(
            profile_id=profile.pk
        )

        if str(new_avatar).endswith('.jpeg', '.jpg', '.png'):
            avatar.image = new_avatar
            avatar.save()
        else:
            return Response('Неверный формат файла', status=status.HTTP_400_BAD_REQUEST)

        return Response('Успешно обновлен', status=status.HTTP_200_OK)


class ChangePassword(GenericAPIView, UpdateModelMixin):
    serializer_class = PasswordChangeSerializer

    def get_object(self):
        return self.request.user

    def post(self, *args, **kwargs):
        return self.update(self.request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.date.get('passwordCurrent')):
                return Response({'passwordCurrent': ['Неверный пароль']},
                                status=status.HTTP_400_BAD_REQUEST)

            elif not serializer.data.get('password') == serializer.data.get('passwordReply'):
                return Response({'password': ['Пароль должен совпадать']},
                                status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get(
                'passwordReply'
            ))
            self.object.save()

            return Response('Успешно обновлен',
                            status=status.HTTP_200_OK)

        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
