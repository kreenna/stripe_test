from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Item(models.Model):
    """Модель товара с названием, описанием, ценой и связанным заказом."""
    CURRENCY_CHOICES = (
        ('usd', 'USD'),
        ('eur', 'EUR'),
        ('rub', 'RUB')
    )

    name = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="rub")

    def __str__(self):
        return f"{self.name} ({self.price} {self.currency.upper()})"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

class Order(models.Model):
    """Модель заказа с полем для создателя, товарами и суммой товаров."""
    items = models.ManyToManyField(Item)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.price for item in self.items.all())

    def __str__(self):
        return f"Заказ {self.id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class Discount(models.Model):
    """Модель скидки, можно прикрепить к заказу (в рублях или в процентах)."""
    reason = models.TextField(verbose_name="Обоснование")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                 verbose_name="Скидка в рублях", null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=4, default=0,
                                     verbose_name="Скидка в процентах", null=True, blank=True)  # от 0.0000 до 0.9999
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL, related_name="discounts")


    def __str__(self):
        return self.reason

    def clean(self):
        # исключить скидку более полной стоимости товара
        if self.percentage > 1:
            raise ValidationError("Скидка не может быть выше полной стоимости товара.")
        # исключить одновременное указание скидки в рублях и процентах
        if self.amount and self.percentage:
            raise ValidationError("Укажите скидку либо в рублях, либо в процентах.")

    @property
    def total_amount(self):
        return self.amount if self.amount else self.order.total_price * self.percentage

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"


class Tax(models.Model):
    """Модель налога, можно прикрепить к заказу."""
    name = models.CharField(max_length=250, verbose_name="Название налога")
    percentage = models.DecimalField(max_digits=5, decimal_places=4, default=0,
                                     verbose_name="Скидка в процентах", null=True, blank=True)  # от 0.0000 до 0.9999
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL, related_name="taxes")

    def __str__(self):
        return self.name

    def clean(self):
        # исключить налог более полной стоимости товара
        if self.percentage > 1:
            raise ValidationError("Скидка не может быть выше полной стоимости товара.")

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"
