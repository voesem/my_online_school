from rest_framework import serializers

from courses.models import Course, Lesson, Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson', many=True, read_only=True)

    def get_lesson_count(self, instance):
        return instance.lesson.count()

    class Meta:
        model = Course
        fields = '__all__'


class PaymentListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
