from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    image = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание', **NULLABLE)
    image = models.ImageField(upload_to='courses/', verbose_name='превью', **NULLABLE)
    url = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, blank=True, verbose_name='курс', related_name='lesson'
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    CASH = 'cash'
    TRANSFER = 'transfer'

    METHODS = (
        (CASH, 'наличные'),
        (TRANSFER, 'перевод на счет'),
    )

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='пользователь', related_name='user'
    )
    date = models.DateField(auto_now_add=True, verbose_name='дата оплаты')
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, blank=True, verbose_name='оплаченный курс', related_name='payment'
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, null=True, blank=True, verbose_name='оплаченный урок', related_name='payment'
    )
    summ = models.IntegerField(verbose_name='сумма оплаты')
    method = models.CharField(max_length=15, choices=METHODS, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.summ}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, blank=True, verbose_name='курс'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='пользователь'
    )

    def __str__(self):
        return f'Подписка {self.user.email} на {self.course.title}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
