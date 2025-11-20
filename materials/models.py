from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()


class Item(models.Model):
    """Модель товара с названием, описанием, ценой и связанным заказом."""
    CURRENCY_CHOICES = (
        ('usd', 'USD'),
        ('rub', 'RUB')
    )

    name = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')

    def __str__(self):
        return f"{self.name} ({self.price} {self.currency.upper()})"

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Discount(models.Model):
    """Модель скидки, можно прикрепить к заказу (в рублях или в процентах)."""
    name = models.TextField(verbose_name="Обоснование")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                 verbose_name="Скидка в центах или копейках", null=True, blank=True)
    currency = models.CharField(max_length=3, choices=[('usd', 'USD'), ('rub', 'RUB')], default='rub')


    def __str__(self):
        return f"{self.name} ({self.amount / 100:.2f} {self.currency.upper()} off)"

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"


class Tax(models.Model):
    """Модель налога, можно прикрепить к заказу."""
    name = models.CharField(max_length=250, verbose_name="Название налога")
    percentage = models.DecimalField(max_digits=5, decimal_places=4, default=0,
                                     verbose_name="Скидка в процентах", null=True, blank=True)  # от 0.0000 до 0.9999

    def __str__(self):
        return self.name

    def clean(self):
        # исключить налог более полной стоимости товара
        if self.percentage > 1:
            raise ValidationError("Скидка не может быть выше полной стоимости товара.")

    class Meta:
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"


class Order(models.Model):
    """Модель заказа с полем для создателя, товарами и суммой товаров."""
    items = models.ManyToManyField(Item)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    discounts = models.ManyToManyField(Discount, null=True, blank=True, related_name="orders")
    taxes = models.ManyToManyField(Tax, null=True, blank=True, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return sum(item.price for item in self.items.all())

    def total_discount_amount(self):
        # Sum of discount amounts for discounts matching the currency of items
        currency = self.items.first().currency if self.items.exists() else 'usd'
        return sum(d.amount for d in self.discounts.all() if d.currency == currency)

    def total_tax_amount(self):
        # Calculate tax on (subtotal - discounts), for taxes matching currency
        currency = self.items.first().currency if self.items.exists() else 'usd'
        subtotal_after_discounts = self.subtotal() - self.total_discount_amount()
        total_tax = 0
        for tax in self.taxes.all():
            if tax.currency == currency:
                total_tax += int(subtotal_after_discounts * float(tax.percentage) / 100)
        return total_tax

    def __str__(self):
        return f"Заказ {self.id}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"