from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render

from .utils import compute_price, get_unique
from .forms import PizzaForm, SaladForm
from .models import Topping, Pizza, Order, Pasta, Salad, Sub, Sub_main, Sub_addon

import logging

logger = logging.getLogger(__name__)

def index(request):
    logger.warning("Here is the index")
    return render(request, "orders/index.html",{})

def menu(request):
    plain_subs = Sub.objects.exclude(addons__isnull=False).order_by('main')

    context = {"Pastas":Pasta.objects.all(),
                "Salads":Salad.objects.all(),
                "Subs": Sub_main.objects.all(),
                "Sub_addons":Sub_addon.objects.all(),
                "Toppings": Topping.objects.all()}
    return render(request, "orders/menu.html",context)

def info(request):
    return render(request, "orders/info.html",{})

def cart(request):
    """This function takes to cart page"""
    order, created = Order.objects.get_or_create(client=request.user,payment_status=False)
    context = {"order":order,
    "price": compute_price(order)}
    return render(request, "orders/cart.html", context) #"Pizza": [str(e) for e in order.pizzas.all()]

def pay(request):
    """This function takes to payment page"""
    context = {"price":request.GET.get('price')}
    return render(request, "orders/payment.html", context)

def get_order(request):
    pizza_form = PizzaForm()
    salad_form = SaladForm()
    return render(request, 'orders/order.html', {'pizza_form': pizza_form, 'salad_form': salad_form})

def order_pizza(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        pizza_form = PizzaForm(request.POST)
        # check whether it's valid:
        if pizza_form.is_valid():
            # process the data in form.cleaned_data as required
            pizza = Pizza.objects.create(pizza_type=pizza_form.cleaned_data['pizza_type'],pizza_size=pizza_form.cleaned_data['pizza_size'])
            for top in pizza_form.cleaned_data['toppings']:
                    top_obj = Topping.objects.get(type=top)
                    pizza.toppings.add(top_obj)
            pizza.save()

            #add to order or create
            order, created = Order.objects.get_or_create(client=request.user,payment_status=False)
            order.pizzas.add(pizza)
            # redirect to a new URL:
            return HttpResponseRedirect('cart')
    else:
        print("Error") #TODO

def order_salad(request):
    logger.warning("I am here")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        salad_form = SaladForm(request.POST)
        logger.warning("there")
        # check whether it's valid:
        if salad_form.is_valid():
            logger.warning(salad_form.cleaned_data["salad_type"])
            # process the data in form.cleaned_data as required
            #salad =  #Salad.objects.get(type=salad_form.cleaned_data['pizza_type'],pizza_size=pizza_form.cleaned_data['pizza_size'])
            #add to order or create
            order, created = Order.objects.get_or_create(client=request.user,payment_status=False)
            order.salads.add(salad_form.cleaned_data["salad_type"])
            # redirect to a new URL:
            return HttpResponseRedirect('cart')
    else:
        return render(request, 'orders/error.html') #TODO

def validate(request):
    """This function take to thank you page"""
    try:
        order = Order.objects.get(client=request.user,payment_status=False)
    except Order.DoesNotExist:
        raise Http404("No order to pay")
    order.payment_status = True
    order.save()
    return render(request,'orders/thankyou.html',{"client": request.user})


def monitor(request):
    """Function to view admin monitoring"""
    #IMPLEMENTER: checkez si la personne est logged en tant qu'admin
    pending = Order.objects.filter(payment_status=True,delivered_status=False)
    return render(request,'orders/admin.html',{"orders":pending})
