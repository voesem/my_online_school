from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import UserSerializer, MyTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ Представление пользователей """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class MyTokenObtainPairView(TokenObtainPairView):
    """ Получение токена при авторизации """

    serializer_class = MyTokenObtainPairSerializer
