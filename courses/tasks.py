from django.conf import settings
from django.core.mail import send_mail
from courses.models import Subscription
from datetime import datetime, timedelta
from celery import shared_task
from users.models import User


@shared_task
def send_mail_user_update(object_pk):
    """ Асинхронная рассылка писем пользователям об обновлении материалов курса """

    subs_list = Subscription.objects.filter(course=object_pk)

    for item in subs_list:
        print(f'Рассылка пользователю {item.user} {item}')
        send_mail(
            subject='Обновление',
            message=f'Обновление курса(ов) {list(subs_list)}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[item.user.email]
        )


@shared_task
def check_user():
    """ Фоновая задача, блокирующая пользователя, если пользователь не заходил более месяца """

    now_date = datetime.now()
    one_month_ago = now_date - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago)
    inactive_users.update(is_active=False)
    print(inactive_users)
