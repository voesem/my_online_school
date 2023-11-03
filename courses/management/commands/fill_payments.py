from django.core.management import BaseCommand

from courses.models import Payment, Lesson, Course
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        Payment.objects.all().delete()
        first_user = User.objects.get(id='1')
        second_lesson = Lesson.objects.get(id='2')
        fourth_course = Course.objects.get(id='4')

        payment_list = [
            {
                'user': first_user,
                'lesson': second_lesson,
                'summ': 1500,
                'method': 'cash'
            },
            {
                'user': first_user,
                'course': fourth_course,
                'summ': 50000,
                'method': 'transfer'
            }
        ]

        payments_for_create = []

        for payment_item in payment_list:
            payments_for_create.append(
                Payment(**payment_item)
            )

        Payment.objects.bulk_create(payments_for_create)
