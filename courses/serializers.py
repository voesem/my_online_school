from rest_framework import serializers

from courses.models import Course, Lesson, Payment, Subscription
from courses.validators import URLValidator


class LessonSerializer(serializers.ModelSerializer):
    url = serializers.CharField(validators=[URLValidator], required=False)

    class Meta:
        model = Lesson
        fields = '__all__'
        # validators = [
        #     URLValidator(field='url'),
        # ]


class CourseSerializer(serializers.ModelSerializer):
    subscribed = serializers.SerializerMethodField()
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson', many=True, read_only=True)

    def get_lesson_count(self, instance):
        return instance.lesson.count()

    def get_subscribed(self, instance):
        request = self.context.get('request')
        if request:
            return Subscription.objects.filter(user=request.user, course=instance).exists()
        return False

    class Meta:
        model = Course
        fields = '__all__'


class PaymentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
