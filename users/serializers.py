from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from courses.serializers import PaymentListSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentListSerializer(source='user', many=True, read_only=True)

    def validate_password(self, value: str) -> str:

        return make_password(value)

    class Meta:
        model = User
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token
