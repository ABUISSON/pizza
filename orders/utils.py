from orders.models import PizzaPrice
from django.shortcuts import get_object_or_404

import logging

logger = logging.getLogger(__name__)

# TODO placer prochaine fonction en attribut du modèle Order
def compute_price(order):
    price = 0
    for pizza in order.pizzas.all():
        price += float(pizza_price(pizza))
    for salad in order.salads.all():
        price += float(salad.price)
    for pasta in order.pastas.all():
        price += float(pasta.price)
    return price

# TODO mettre celle ci en méthode dans Pizza
def pizza_price(pizza):
    k = min(4,len(pizza.toppings.all()))
    price_obj = get_object_or_404(PizzaPrice, pizza_type=pizza.pizza_type,pizza_size=pizza.pizza_size,n_tops=k)
    return price_obj.price

def get_unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
