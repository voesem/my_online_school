from rest_framework import serializers

from courses.serializers import PaymentListSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentListSerializer(source='user', many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
