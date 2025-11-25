import stripe
from django.conf import settings

from .models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY  # секретный ключ Stripe


def create_payment_intent(request, order_id):
    """Функция для создания Stripe Payment Intent."""

    order = Order.objects.get(id=order_id)  # получаем нужный заказ

    amount = int(order.total_price() * 100)  # рассчитываем сумму в минимальных единицах
    currency = order.items.first().currency if order.items.exists() else "rub"  # валюта из первого товара в заказе

    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        payment_method_types=["card"],  # поддерживаемые типы оплаты
        metadata={"Заказ": str(order.id)},
        description=f"{order}",
    )

    return str(payment_intent.client_secret)
