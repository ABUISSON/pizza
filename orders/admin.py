from django.contrib import admin

from .models import DishType, Topping, Pizza, Order
# Register your models here.
admin.site.register(DishType)
admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(Order)
