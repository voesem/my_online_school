import requests
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


# def create_customer(user):
#     customer = stripe.Customer.create(
#         email=user.email
#     )
#
#     return customer

def checkout_session(course, user):
    headers = {'Authorization': f'Bearer {stripe.api_key}'}
    data = [
        ('amount', course.amount),
        ('currency', 'rub'),
    ]

    response = requests.post(f'{settings.STRIPE_URL}/payment_intents', headers=headers, data=data)

    if response.status_code != 200:
        raise Exception(f'ошибка : {response.json()["error"]["message"]}')

    return response.json()


def create_payment(amount, customer, instance):
    """ Создание платежа Stripe API """

    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency="rub",
        automatic_payment_methods={"enabled": True},
        description=f'Оплата за {instance} от {customer}'
    )

    return payment_intent


def get_payment(payment_id):
    """ Получение информации о платеже Stripe API """

    payment_info = stripe.PaymentIntent.retrieve(
        id=payment_id
    )

    return payment_info
