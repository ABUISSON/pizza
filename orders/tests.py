from django.test import TestCase
from .models import Topping, Pizza, PizzaPrice, Sub_addon, Sub_main, Sub, Pasta, Salad, Plate, Order

class OrderTestCase(TestCase):

    def setUp(self):
        #create toppings
        t1 = Topping.objects.create(type="Kebab")
        t2 = Topping.objects.create(type="Grenouille")

        #create pizza
        p1 = Pizza.objects.create(pizza_type='R',pizza_size='S')
        p2 = Pizza.objects.create(pizza_type='S',pizza_size='L')
        p2.toppings.add(t1)
        p2.toppings.add(t2)

        #create prices
        PizzaPrice.objects.create(pizza_type='R',pizza_size='S',n_tops=0,price=5)
        PizzaPrice.objects.create(pizza_type='S',pizza_size='L',n_tops=2,price=30)

        #create order
        o1 = Order.objects.create()
        o1.pizzas.add(p1)
        o1.pizzas.add(p2)

    def test_pizza_toppings(self):
        p = Pizza.objects.get(pizza_type='S',pizza_size='L')
        self.assertEqual(p.toppings.count(), 2)

    def test_pizza_price(self):
        p = Pizza.objects.get(pizza_type='S',pizza_size='L')
        p_price = PizzaPrice.objects.get(pizza_type='S',pizza_size='L')
        self.assertEqual(p_price.price,30)

    def test_order_size(self):
        o = Order.objects.get(payment_status=False,delivered_status=False)
        self.assertEqual(o.get_order_size(), 2)

    def test_order_food(self):
        o = Order.objects.get(payment_status=False,delivered_status=False)
        p1 = Pizza.objects.get(pizza_type='R',pizza_size='S')
        p2 = Pizza.objects.get(pizza_type='S',pizza_size='L')
        self.assertEqual(o.all_food(), [str(p1),str(p2)])
