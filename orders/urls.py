from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_order, name="order"),
    path("cart", views.cart, name="cart"),
    path("payment/",views.pay, name="pay"),
    path("validate_payment",views.validate, name="validate")
    #path("order", views.order, name="order")
]
