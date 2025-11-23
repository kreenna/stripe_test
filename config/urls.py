from django.contrib import admin
from django.urls import path

from materials.views import BuyView, item_view

urlpatterns = [
    path("admin/", admin.site.urls),

    path("buy/<int:id>/", BuyView.as_view(), name="buy"),
    path("item/<int:id>/", item_view, name="item"),
]
