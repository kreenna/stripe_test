import stripe
from django.conf import settings
from django.http import JsonResponse

from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY  # секретный ключ Stripe


def create_payment_intent(request, order_id):
    order = Order.objects.get(id=order_id)  # получаем нужный заказ

    amount = order.total_price() * 100  # рассчитываем сумму в минимальных единицах
    currency = order.items.first().currency if order.items.exists() else "rub"  # валюта из первого товара в заказе

    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        payment_method_types=["card"],  # поддерживаемые типы оплаты
        metadata={"Заказ": str(order.id)},
        description=f"{order}",
    )

    return JsonResponse({"clientSecret": payment_intent.client_secret})
