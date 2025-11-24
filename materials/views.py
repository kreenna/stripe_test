from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .models import Item, Order
from .services import create_payment_intent


def item_view(request, id):
    """Простое отображение страницы товара."""
    item = Item.objects.get(id=id)
    return render(request, "item.html", {
        "item": item,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
    })


class BuyView(View):
    """View для покупки товара при нажатии на Buy."""

    def get(self, request, id):
        item = Item.objects.get(id=id)
        order = Order.objects.create()
        order.items.add(item)
        order.save()

        client_secret = create_payment_intent(request, order.id)  # получение client_secret
        return JsonResponse({"clientSecret": client_secret})
