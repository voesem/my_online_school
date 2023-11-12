from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from courses.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create(email='user@test.com', password='test')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test_course',
            description='test_course',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            title='test_lesson',
            description='test_lesson',
            course=self.course,
            url='http://www.youtube.com/test_lesson',
            owner=self.user
        )

    def test_crate_lesson(self):
        """ Тест создания урока """

        data = {
            'title': 'Урок пятый',
            'description': 'Это пятый по урок по HTML',
            'url': 'https://www.youtube.com/watch?v=gL-QqUND0nw',
            'course': self.course.pk
        }

        response = self.client.post(
            reverse('courses:create_lesson'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_lesson_list(self):
        """ Тест списка уроков """

        response = self.client.get(
            reverse('courses:lesson_list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.lesson.pk,
                        'title': self.lesson.title,
                        'description': self.lesson.description,
                        'image': None,
                        'url': self.lesson.url,
                        'course': self.course.pk,
                        'owner': self.user.pk
                    }
                ]

            }
        )

    def test_lesson_retrieve(self):
        """ Тест вывода одного урока """
        response = self.client.get(
            reverse('courses:lesson_get', kwargs={'pk': self.lesson.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.pk,
                'title': self.lesson.title,
                'description': self.lesson.description,
                'image': None,
                'url': self.lesson.url,
                'course': self.course.pk,
                'owner': self.user.pk
            }
        )

    def test_lesson_update(self):
        """ Тест изменения урока """

        data = {
            'description': 'test_lesson_updated'
        }

        response = self.client.patch(
            reverse('courses:lesson_update', kwargs={'pk': self.lesson.pk}),
            data=data
        )

        print(response)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'id': self.lesson.pk,
                'title': self.lesson.title,
                'description': 'test_lesson_updated',
                'image': None,
                'url': self.lesson.url,
                'course': self.course.pk,
                'owner': self.user.pk
            }
        )

    def test_delete(self):
        """ Тест удаления урока """

        response = self.client.delete(
            reverse('courses:lesson_delete', kwargs={'pk': self.lesson.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='user@test.com', password='test')
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(
            title='test_course',
            description='test_course',
            owner=self.user
        )

    def test_create(self):
        """ Тест создания подписки """

        subscription = {
            "user": self.user.pk,
            "course": self.course.pk
        }

        response = self.client.post(
            reverse('courses:subscription_create', kwargs={'pk': self.course.pk}),
            data=subscription
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_delete(self):
        """ Тест удаления подписки """

        course = Subscription.objects.create(
            user=self.user,
            course=self.course
        )

        response = self.client.delete(
            reverse('courses:subscription_delete', kwargs={'pk': course.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
