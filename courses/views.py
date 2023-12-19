from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.models import Course, Lesson, Payment, Subscription
from courses.paginators import CoursePaginator, LessonPaginator
from courses.permissions import IsOwner, IsModerator, IsNotModerator, IsSubscriber
from courses.serializers import CourseSerializer, LessonSerializer, PaymentListSerializer, SubscriptionSerializer, \
    PaymentSerializer
from courses.services import create_payment, get_payment
from courses.tasks import send_mail_user_update


class CourseViewSet(viewsets.ModelViewSet):
    """ Представление курсов """

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CoursePaginator

    def get_queryset(self):

        if self.request.user.groups.filter(name='Модераторы').exists():
            return Course.objects.all()

        return Course.objects.filter(owner=self.request.user)

    def get_permissions(self):
        """ Права доступа для разных категорий пользователей """

        permission_classes = ()

        if self.action == 'create':
            permission_classes = (IsNotModerator,)  # Модератор не может создавать курсы

        elif self.action == 'destroy':
            permission_classes = (IsOwner,)  # Удалять курсы может только владелец

        elif self.action == 'update' or self.action == 'partial_update':
            permission_classes = (IsNotModerator,)  # Модератор не может редактировать курсы

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """ При создании курса устанавливается связь с текущим пользователем """

        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        """ При редактировании курса пользователю приходит уведомление """

        self.object = serializer.save()
        send_mail_user_update(self.object.pk)


class LessonCreateAPIView(generics.CreateAPIView):
    """ Создание уроков """

    serializer_class = LessonSerializer
    permission_classes = [IsNotModerator]

    def perform_create(self, serializer):
        """ При создании урока устанавливается связь с текущим пользователем """

        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """ Список уроков """

    serializer_class = LessonSerializer
    pagination_class = LessonPaginator

    def get_queryset(self):
        if self.request.user.groups.filter(name='Модераторы').exists():
            return Lesson.objects.all()  # Модераторам доступен список всех уроков

        return Lesson.objects.filter(owner=self.request.user)  # Обычным пользователям доступны только их уроки


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Просмотр уроков """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Редактирование уроков """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsNotModerator]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Удаление уроков """

    queryset = Lesson.objects.all()
    permission_classes = [IsNotModerator]


class PaymentCreateView(generics.CreateAPIView):
    """ Создание платежа """

    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        """ При создании платежа устанавливается связь с текущим пользователем """

        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        # Создание объекта Payment Intent Stripe API
        payment = create_payment(
            amount=serializer.validated_data['summ'],
            instance=serializer.validated_data['course'],
        )

        # Вовзращает id платежа, который можно использовать при запросе ифнормации о платеже
        return Response(payment['id'], status=status.HTTP_201_CREATED)


class PaymentListAPIView(generics.ListAPIView):
    """ Список платежей уроков """

    serializer_class = PaymentListSerializer
    queryset = Payment.objects.all()

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'method',)
    ordering_fields = ('date',)


class GetPaymentView(APIView):
    """
    Получение информации о платеже.
    """

    def get(self, request, payment_id):
        payment_intent = get_payment(payment_id)

        return Response({'status': payment_intent.status})


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """ Создание подписки """

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer, *args, **kwargs):
        """ При создании подписки устанавливается связь с текущим пользователем и курсом """

        new_subscription = serializer.save()
        new_subscription.user = self.request.user
        pk = self.kwargs.get('pk')
        new_subscription.course = Course.objects.get(pk=pk)
        new_subscription.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """ Удаление подписки """

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsSubscriber]
