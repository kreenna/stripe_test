from django.contrib import admin

from .models import Item, Tax, Discount, Order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """Отображение Товара в админке."""
    list_display = ("id", "name", "description", "price", "currency")
    list_filter = ("currency",)
    search_fields = ("name",)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    """Отображение Скидки в админке."""
    list_display = ("id", "name", "amount")
    search_fields = ("amount",)


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    """Отображение Налога в админке."""
    list_display = ("id", "name", "percentage")
    search_fields = ("name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Отображение Заказа в админке."""
    list_display = ("id", "created_at", "subtotal_display", "total_discount_amount_display",
                    "total_tax_amount_display", "total_price_display")
    filter_horizontal = ("items", "discounts", "taxes")
    readonly_fields = ("subtotal_display", "total_discount_amount_display", "total_tax_amount_display",
                       "total_price_display")

    def subtotal_display(self, obj):
        """Отображение суммы всех товаров."""
        return f"{obj.subtotal()}"

    subtotal_display.short_description = "Subtotal"

    def total_discount_amount_display(self, obj):
        """Отображение суммы всех скидок."""
        return f"{obj.total_discount_amount()}"

    total_discount_amount_display.short_description = "Сумма скидок"

    def total_tax_amount_display(self, obj):
        """Отображение суммы всех налогов."""
        return f"{obj.total_tax_amount()}"

    total_tax_amount_display.short_description = "Сумма налогов"

    def total_price_display(self, obj):
        """Отображение итоговой суммы со скидками и налогами."""
        return f"{obj.total_price()}"

    total_price_display.short_description = "Итоговая стоимость"
