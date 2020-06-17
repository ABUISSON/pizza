from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# class DishType(models.Model):
#     type = models.CharField(max_length=64)

############
## PIZZA ###
############

class Topping(models.Model):
    type = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.type}"

PIZZA_TYPES = (
('R','Regular'),
('S', 'Sicilian')
)
PIZZA_SIZES = (
('S','Small'),
('L','Large')
)

class Pizza(models.Model):
    pizza_type = models.CharField(max_length=1, choices=PIZZA_TYPES)
    pizza_size = models.CharField(max_length=1, choices=PIZZA_SIZES)
    toppings = models.ManyToManyField(Topping)
    def __str__(self):
        top_str=""
        for e in self.toppings.all():
            top_str+=str(e)+" "
        return f"Pizza {self.pizza_type} of size {self.pizza_size} with " + top_str


class PizzaPrice(models.Model):
    pizza_type = models.CharField(max_length=1, choices=PIZZA_TYPES)
    pizza_size = models.CharField(max_length=1, choices=PIZZA_SIZES)
    n_tops = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    price = models.DecimalField(max_digits=6, decimal_places=2)

############
## SUBS ###
############

class Sub_addons(models.Model):
    type = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)

SUB_SIZES = (
('S','Small'),
('L','Large')
)

class Sub(models.Model):
    main = models.CharField(max_length=64)
    size = models.CharField(max_length=1, choices=SUB_SIZES)
    addons = models.ManyToManyField(Sub_addons)

############
## PASTA ###
############

class Pasta(models.Model):
    type = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)

############
## SALADS ###
############

class Salad(models.Model):
    type = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)

############
## PLATES ##
############

PLATE_SIZES = (
('S','Small'),
('L','Large')
)

class Plate(models.Model):
    type = models.CharField(max_length=64)
    size = models.CharField(max_length=1, choices=PLATE_SIZES)

############
## GENERAL #
############

class Order(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #food = models.ManyToManyField(Pizza)
    pizzas = models.ManyToManyField(Pizza)
    subs = models.ManyToManyField(Sub)
    pastas = models.ManyToManyField(Pasta)
    salads = models.ManyToManyField(Salad)
    plates = models.ManyToManyField(Plate)
    payment_status = models.BooleanField(default=False)
    delivered_status = models.BooleanField(default=False)
