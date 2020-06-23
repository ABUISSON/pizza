from django.urls import path

from . import views

app_name="orders"

urlpatterns = [
    path("", views.index, name="index"),
    path("menu", views.menu, name="menu"),
    path("order", views.get_order, name="order"),
    path("cart", views.cart, name="cart"),
    path("info", views.info, name="info"),
    path("payment/",views.pay, name="pay"),
    path("validate_payment",views.validate, name="validate"),
    path("monitor", views.monitor, name="monitor"),
    path("order_pizza", views.order_pizza, name="order_pizza"),
    path("order_salad", views.order_salad, name="order_salad"),
    path(r'^done/(?P<pk>[0-9]+)/$', views.done, name='done')
]
