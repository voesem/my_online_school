from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated

from courses.models import Course, Lesson, Payment
from courses.permissions import IsOwner, IsModerator, IsNotModerator
from courses.serializers import CourseSerializer, LessonSerializer, PaymentListSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()

        return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):

        permission_classes = ()

        if self.action == 'create':
            permission_classes = (IsNotModerator,)

        elif self.action == 'destroy':
            permission_classes = (IsOwner,)

        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = (IsNotModerator,)

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsNotModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()

        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsNotModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsNotModerator]


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentListSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method',)
    ordering_fields = ('date',)
