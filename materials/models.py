from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Item(models.Model):
    """Модель товара с названием, описанием, ценой и связанным заказом."""
    name = models.CharField(max_length=250, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Цена")
    currency = models.CharField(max_length=3, choices=[("usd", "USD"), ("eur", "EUR")], default="usd")

    def __str__(self):
        """Метод для вывода товара и его цены."""
        return f"{self.name} ({self.price} {self.currency.upper()})"

    class Meta:
        """Отображение модели."""
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Discount(models.Model):
    """Модель скидки, можно прикрепить к заказу (в рублях или долларах)."""
    name = models.TextField(verbose_name="Обоснование")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                 verbose_name="Скидка в евро или долларах")

    def __str__(self):
        """Метод для вывода скидки."""
        return f"{self.name} ({self.amount} {self.currency.upper()})"

    class Meta:
        """Отображение модели."""
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"


class Tax(models.Model):
    """Модель налога, можно прикрепить к заказу."""
    name = models.CharField(max_length=250, verbose_name="Название налога")
    percentage = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                             default=0, verbose_name="Процент налога")

    def __str__(self):
        """Метод для вывода налога."""
        return self.name

    class Meta:
        """Отображение модели."""
        verbose_name = "Налог"
        verbose_name_plural = "Налоги"


class Order(models.Model):
    """Модель заказа с полем для создателя, товарами и суммой товаров."""
    items = models.ManyToManyField(Item)
    discounts = models.ManyToManyField(Discount, related_name="orders")
    taxes = models.ManyToManyField(Tax, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        """Метод для расчета суммы всех товаров (в евро или долларах)."""
        return sum(item.price for item in self.items.all())

    def total_discount_amount(self):
        """Метод для определения суммы всех скидок (в евро или долларах)."""
        # сумма всех скидок, соответствующая валюте товаров
        currency = self.items.first().currency if self.items.exists() else "usd"
        return sum(discount.amount for discount in self.discounts.all() if discount.currency == currency)

    def price_discounted(self):
        """Метод для определения суммы со скидкой (в евро или долларах)."""
        return self.subtotal() - self.total_discount_amount()

    def total_tax_amount(self):
        """Метод для определения суммы всех налогов (в евро или долларах)."""
        # рассчитываем сумму налога относительно суммы с уже примененной скидкой
        total_tax = 0
        for tax in self.taxes.all():
            total_tax += int(self.price_discounted() * float(tax.percentage) / 100)
        return total_tax

    def total_price(self):
        """Метод для определения конечной суммы к оплате (в евро или долларах)."""
        return int(self.price_discounted()) + self.total_tax_amount()

    def __str__(self):
        """Метод для вывода заказа."""
        return f"Заказ {self.id}"

    class Meta:
        """Отображение модели."""
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
