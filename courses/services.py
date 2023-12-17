import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


# def checkout_session(payment):
#     checkout_session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=[
#             {
#                 'price_data': {
#                     'currency': 'rub',
#                     'unit_amount': payment['summ'],
#                     'product_data': {
#                         'name': payment['course'],
#                     },
#                 },
#                 'quantity': 1
#             }
#         ],
#         mode='payment',
#         success_url=settings.DOMAIN + '?session_id={CHECKOUT_SESSION_ID}',
#         cancel_url=settings.DOMAIN
#     )
#
#     return checkout_session


def create_payment(amount, instance):
    """ Создание платежа Stripe API """

    payment_intent = stripe.PaymentIntent.create(
        payment_method_types=['card'],
        amount=amount,
        currency='rub',
        confirm=True,
        payment_method='pm_card_visa',
        description=f'Оплата за {instance}'
    )

    return payment_intent


def get_payment(payment_id):
    """ Получение информации о платеже Stripe API """

    payment_info = stripe.PaymentIntent.retrieve(
        id=payment_id
    )

    return payment_info
