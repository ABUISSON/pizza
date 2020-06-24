from django.contrib import admin

from .models import Topping, Pizza, Order, PizzaPrice, Sub_addon, Sub_main, Sub, Pasta, Salad, Plate, SaladOrder

# Register your models here.
#admin.site.register(DishType)
admin.site.register(Topping)
admin.site.register(Pizza)
admin.site.register(Order)
admin.site.register(PizzaPrice)
admin.site.register(Sub_addon)
admin.site.register(Sub_main)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Plate)
admin.site.register(SaladOrder)
