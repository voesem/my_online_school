from django.urls import path
from rest_framework.routers import DefaultRouter

from courses.apps import CoursesConfig
from courses.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, SubscriptionCreateAPIView, \
    SubscriptionDestroyAPIView, PaymentCreateView, GetPaymentView

app_name = CoursesConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='create_lesson'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/create/', PaymentCreateView.as_view(), name='create_payment'),
    path('payment/<str:payment_id>/', GetPaymentView.as_view(), name='view_payment'),

    path('courses/<int:pk>/create_sub/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('courses/<int:pk>/delete_sub/', SubscriptionDestroyAPIView.as_view(), name='subscription_delete'),
] + router.urls
