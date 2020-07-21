from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404

class RightsSupport(models.Model):
    class Meta:
        managed = False  # No database table creation or deletion  \
                         # operations will be performed for this model.

        default_permissions = () # disable "add", "change", "delete"
                                 # and "view" default permissions

        permissions = (
            ('see_monitor', 'STAFF rights to monitor'),
            ('client', 'Client rights')
        )


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

    def get_price(self):
        k = min(4,len(self.toppings.all()))
        price_obj = get_object_or_404(PizzaPrice, pizza_type=self.pizza_type,pizza_size=self.pizza_size,n_tops=k)
        return price_obj.price

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

    def get_price(self):
        """
        Obtaning the price of the Sub object based on the main sub and
        its addons.
        """
        price_main = get_object_or_404(Sub_main, name=self.main.name)
        if self.size == 'S':
            price = price_main.price_s
        else:
            price = price_main.price_l
        # TODO checker que l'object price contient price_s et price_l ?
        for addon in self.addons.all():
            temp = get_object_or_404(Sub_addon, type=addon.type)
            price += temp.price
        return price

    def __str__(self):
        addons_str=""
        for e in self.addons.all():
            addons_str += str(e) + " "
        return f"Sub {self.main} of size {self.size} with " + addons_str

############
## PASTA ###
############

class Pasta(models.Model):
    type = models.CharField(max_length=64, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return f"{self.type}"

class PastaOrder(models.Model):
    """
    Additional table for the many-to-many relation between Pasta and Order
    objects
    """
    pasta = models.ForeignKey(Pasta, on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.pasta}"

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
    pastas = models.ManyToManyField(Pasta, through=PastaOrder)
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

    def all_food(self):
        all_food = []
        for p in self.pizzas.all():
            all_food.append(str(p))
        for p in self.subs.all():
            all_food.append(str(p))
        for p in self.pastas.all():
            all_food.append(str(p))
        for p in self.salads.all():
            all_food.append(str(p))
        for p in self.plates.all():
            all_food.append(str(p))
        return all_food

    def compute_price(self):
        price = 0
        for pizza in self.pizzas.all():
            price += float(pizza.get_price())
        for salad in self.salads.all():
            price += float(salad.price)
        for pasta in self.pastas.all():
            price += float(pasta.price)
        for sub in self.subs.all():
            price += float(sub.get_price())
        return price

    def __str__(self):
        pizz_str = ", ".join(str(p) for p in self.pizzas.all())
        subs_str = ", ".join(str(p) for p in self.subs.all())
        pasta_str = ", ".join(str(p) for p in self.pastas.all())
        salad_str = ", ".join(str(p) for p in self.salads.all())
        plates_str = ", ".join(str(p) for p in self.plates.all())
        return f"{self.client} paid : {self.payment_status} content : {pizz_str} \ {subs_str} \ {pasta_str} \ {salad_str} \ {plates_str}"
