from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

############
## PIZZA ###
############

class Topping(models.Model):
    type = models.CharField(max_length=64, unique=True)
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
    toppings = models.ManyToManyField(Topping, blank=True)
    def __str__(self):
        top_str=""
        for e in self.toppings.all():
            top_str+=str(e)+" "
        return f"Pizza {self.pizza_type} of size {self.pizza_size} with " + top_str


class PizzaPrice(models.Model):
    pizza_type = models.CharField(max_length=1, choices=PIZZA_TYPES)
    pizza_size = models.CharField(max_length=1, choices=PIZZA_SIZES)
    n_tops = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(5)])
    price = models.DecimalField(max_digits=6, decimal_places=2)
    class Meta:
        unique_together = ["pizza_type", "pizza_size", "n_tops"]
    def __str__(self):
        return f"Pizza {self.pizza_type} of size {self.pizza_size} with {self.n_tops} toppings"

############
## SUBS ###
############

class Sub_addon(models.Model):
    type = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return f"{self.type}"

SUB_SIZES = (
('S','Small'),
('L','Large')
)

class Sub_main(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price_s = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    price_l = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    def __str__(self):
        return f"{self.name}"

class Sub(models.Model):
    main = models.ForeignKey(Sub_main, on_delete=models.CASCADE)
    size = models.CharField(max_length=1, choices=SUB_SIZES)
    addons = models.ManyToManyField(Sub_addon, blank=True)
    price = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    def __str__(self):
        return f"{self.main}"

############
## PASTA ###
############

class Pasta(models.Model):
    type = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return f"{self.type}"

############
## SALADS ###
############

class Salad(models.Model):
    type = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return f"{self.type}"


class SaladOrder(models.Model):
    salad = models.ForeignKey(Salad, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.salad}"

############
## PLATES ##
############

PLATE_SIZES = (
('S','Small'),
('L','Large')
)

class Plate(models.Model):
    type = models.CharField(max_length=64, unique=True)
    size = models.CharField(max_length=1, choices=PLATE_SIZES)
    def __str__(self):
        return f"{self.type}"

############
## GENERAL #
############

class Order(models.Model):
    #TODO Ajouter un timestamp
    client = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True)
    pizzas = models.ManyToManyField(Pizza)
    subs = models.ManyToManyField(Sub)
    pastas = models.ManyToManyField(Pasta)
    salads = models.ManyToManyField(Salad, through=SaladOrder)
    plates = models.ManyToManyField(Plate)
    payment_status = models.BooleanField(default=False)
    delivered_status = models.BooleanField(default=False)

    def get_order_size(self):
        n_piz = self.pizzas.count()
        n_sub = self.subs.count()
        n_pas = self.pastas.count()
        n_sal = self.salads.count()
        n_pla = self.plates.count()
        return n_piz+n_sub+n_pas+n_sal+n_pla
        
    def __str__(self):
        pizz_str = ", ".join(str(p) for p in self.pizzas.all())
        subs_str = ", ".join(str(p) for p in self.subs.all())
        pasta_str = ", ".join(str(p) for p in self.pastas.all())
        salad_str = ", ".join(str(p) for p in self.salads.all())
        plates_str = ", ".join(str(p) for p in self.plates.all())
        return f"{self.client} paid : {self.payment_status} content : {pizz_str} \ {subs_str} \ {pasta_str} \ {salad_str} \ {plates_str}"
