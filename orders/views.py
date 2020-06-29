from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404

from .utils import compute_price, get_unique
from .forms import PizzaForm, SaladForm, PastaForm
from .models import Topping, Pizza, Order, Pasta, Salad, Sub, Sub_main, Sub_addon, SaladOrder, PizzaPrice, PastaOrder

import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, "orders/index.html",{})

def menu(request):
    #data on subs
    plain_subs = Sub.objects.exclude(addons__isnull=False).order_by('main')
    #data on pizzas
    regular_prices={}
    for n_tops in range(5):
        regular_prices[n_tops] = []
        for size in ['S','L']:
              p = PizzaPrice.objects.get(pizza_type='R',pizza_size=size,n_tops=n_tops).price
              #TODO ajouter des choses pour vérifier que ça se passe bien (requete existe et unique)
              regular_prices[n_tops].append(p)
    sicilian_prices={}
    for n_tops in range(5):
        sicilian_prices[n_tops] = []
        for size in ['S','L']:
              p = PizzaPrice.objects.get(pizza_type='S',pizza_size=size,n_tops=n_tops).price
              #TODO ajouter des choses pour vérifier que ça se passe bien
              sicilian_prices[n_tops].append(p)

    context = {"Pastas":Pasta.objects.all(),
                'Pizza_header':['', 'Small','Large'],
                'R_rows':regular_prices,
                'S_rows':sicilian_prices,
                "Salads":Salad.objects.all(),
                "Subs": Sub_main.objects.all(),
                "Sub_addons":Sub_addon.objects.all(),
                "Toppings": Topping.objects.all()}
    return render(request, "orders/menu.html",context)

def info(request):
    return render(request, "orders/info.html",{})

def cart(request):
    """This function takes to cart page"""
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(client=request.user,payment_status=False) #TODO doit-on garder ces create ?
        context = {"order":order,
        "price": compute_price(order)}
    else:
        if 'order_id' in request.session:
            order = Order.objects.get(pk=request.session['order_id'])
            context = {"order":order,
            "price": compute_price(order)}
        else:
            context = {"order":"No order yet",
                        "price":0}
    return render(request, "orders/cart.html", context)

def pay(request):
    """This function takes to payment page"""
    if request.user.is_authenticated:
        context = {"price":request.GET.get('price')}
        return render(request, "orders/payment.html", context)
    else:
        request.session['order_finished'] = True
        return render(request, "users/login.html", {"message": "Log in to validate your order"})

def get_order(request):
    pizza_form = PizzaForm()
    salad_form = SaladForm()
    pasta_form = PastaForm()
    return render(request, 'orders/order.html',
            {'pizza_form': pizza_form, 'salad_form': salad_form,
             'pasta_form': pasta_form})

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
            if request.user.is_authenticated:
                order, created = Order.objects.get_or_create(client=request.user,payment_status=False)
            else:
                if 'order_id' in request.session:
                    pk = request.session['order_id']
                    order = Order.objects.get(pk=pk)
                else:
                    order = Order(payment_status=False)
                    order.save()
                    request.session['order_id']=order.pk
            order.pizzas.add(pizza)
            # redirect to a new URL:
            return HttpResponseRedirect('cart')
        else:
            pass #TODO
    else:
        logger.warning("Error") #TODO

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
            #order.salads.add(salad_form.cleaned_data["salad_type"])
            s = SaladOrder(salad=salad_form.cleaned_data["salad_type"], order=order)
            s.save()
            # redirect to a new URL:
            return HttpResponseRedirect('cart')
    else:
        return render(request, 'orders/error.html') #TODO

def order_pasta(request):
    logger.warning("I am in order_pasta")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        pasta_form = PastaForm(request.POST)
        logger.warning("there")
        # check whether it's valid:
        if pasta_form.is_valid():
            logger.warning(pasta_form.cleaned_data["pasta_type"])
            # process the data in form.cleaned_data as required
            #salad =  #Salad.objects.get(type=salad_form.cleaned_data['pizza_type'],pizza_size=pizza_form.cleaned_data['pizza_size'])
            #add to order or create
            order, created = Order.objects.get_or_create(client=request.user,payment_status=False)
            p = PastaOrder(pasta=pasta_form.cleaned_data["pasta_type"], order=order)
            p.save()
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

def done(request,pk):
    """ Function to set orders to completed """
    order = get_object_or_404(Order,pk=pk)
    if request.method == 'POST':
        order.delivered_status = True
        order.save()
    pending = Order.objects.filter(payment_status=True,delivered_status=False)
    return render(request,'orders/admin.html',{"orders":pending})
