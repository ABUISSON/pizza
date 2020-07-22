from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required

from .forms import PizzaForm, SaladForm, PastaForm, SubForm, PlateForm
from .models import Topping, Pizza, Order, Pasta, Salad, Sub, Sub_main, Sub_addon, Plate, PlateOrder, SaladOrder, PizzaPrice, PastaOrder

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
        context = {"order":order.all_food(),
        "price": order.compute_price()}
    else:
        if 'order_id' in request.session:
            order = Order.objects.get(pk=request.session['order_id'])
            context = {"order":order.all_food(),
            "price": order.compute_price()}
        else:
            context = {"order":["No order yet"],
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
    pizza_form = PizzaForm({'pizza_type':'R','pizza_size':'S'})
    salad_form = SaladForm()
    pasta_form = PastaForm()
    sub_form = SubForm()
    plate_form = PlateForm()
    return render(request, 'orders/order.html',
            {'pizza_form': pizza_form, 'salad_form': salad_form,
             'pasta_form': pasta_form, 'sub_form':sub_form,
             'plate_form': plate_form})

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
        return render(request, 'orders/error.html') #TODO ajouter page erreur

def order_salad(request):
    logger.warning("I am in salad")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        salad_form = SaladForm(request.POST)
        # check whether it's valid:
        if salad_form.is_valid():
            logger.warning(salad_form.cleaned_data["salad_type"])
            # process the data in form.cleaned_data as required
            #add to order or create
            if request.user.is_authenticated:
                order, created = Order.objects.get_or_create(
                                    client=request.user,payment_status=False)
            else:
                if 'order_id' in request.session:
                    pk = request.session['order_id']
                    order = Order.objects.get(pk=pk)
                else:
                    order = Order(payment_status=False)
                    order.save()
                    request.session['order_id']=order.pk

            s = SaladOrder(salad=salad_form.cleaned_data["salad_type"], order=order)
            s.save()
            # redirect to a new URL:
            return HttpResponseRedirect('cart')
    else:
        return render(request, 'orders/error.html') #TODO

def order_pasta(request):
    # TODO: gérer quand on est pas loggé.
    logger.warning("I am in order_pasta")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        pasta_form = PastaForm(request.POST)
        logger.warning("there")
        # check whether it's valid:
        if pasta_form.is_valid():
            logger.warning(pasta_form.cleaned_data["pasta_type"])
            # process the data in form.cleaned_data as required
            if request.user.is_authenticated:
                order, created = Order.objects.get_or_create(
                                    client=request.user,payment_status=False)
            else:
                if 'order_id' in request.session:
                    pk = request.session['order_id']
                    order = Order.objects.get(pk=pk)
                else:
                    order = Order(payment_status=False)
                    order.save()
                    request.session['order_id']=order.pk
            p = PastaOrder(pasta=pasta_form.cleaned_data["pasta_type"], order=order)
            p.save()
            # redirect to a new URL:
            return HttpResponseRedirect('cart')
    else:
        return render(request, 'orders/error.html') #TODO

def order_sub(request):
    logger.warning("I am in order_sub")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        sub_form = SubForm(request.POST)
        # check whether it's valid:
        if sub_form.is_valid():
            logger.warning(sub_form.cleaned_data["sub_main"])
            # process the data in form.cleaned_data as required
            sub = Sub.objects.create(main=sub_form.cleaned_data['sub_main'],
                                     size=sub_form.cleaned_data['sub_size'])
            for top in sub_form.cleaned_data["toppings"]:
                top_obj = Sub_addon.objects.get(type=top)
                sub.addons.add(top_obj)
            sub.save()
            #add to order or create
            if request.user.is_authenticated:
                order, created = Order.objects.get_or_create(
                                    client=request.user,payment_status=False)
            else:
                if 'order_id' in request.session:
                    pk = request.session['order_id']
                    order = Order.objects.get(pk=pk)
                else:
                    order = Order(payment_status=False)
                    order.save()
                    request.session['order_id']=order.pk
            order.subs.add(sub)
            # redirect to a new URL:
            return HttpResponseRedirect('cart')
    else:
        return render(request, 'orders/error.html') #TODO

def order_plate(request):
    logger.warning("I am in order_plate")
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        plate_form = PlateForm(request.POST)
        # check whether it's valid:
        if plate_form.is_valid():
            logger.warning(plate_form.cleaned_data["type"])
            # process the data in form.cleaned_data as required
            plate = Plate.objects.get(type=plate_form.cleaned_data["type"],
                            size = plate_form.cleaned_data['plate_size'])

            #add to order or create
            if request.user.is_authenticated:
                order, created = Order.objects.get_or_create(
                                    client=request.user,payment_status=False)
            else:
                if 'order_id' in request.session:
                    pk = request.session['order_id']
                    order = Order.objects.get(pk=pk)
                else:
                    order = Order(payment_status=False)
                    order.save()
                    request.session['order_id']=order.pk

            plate_order = PlateOrder(plate=plate, order=order)
            plate_order.save()
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

@permission_required('orders.see_monitor', raise_exception=True)
def monitor(request):
    """Function to view admin monitoring"""
    #TODO: checkez si la personne est logged en tant qu'admin
    #TODO : ajouter aux tests
    pending = Order.objects.filter(payment_status=True,delivered_status=False).all()
    orders = []
    for o in pending:
        orders.append({"order":o,"food":o.all_food()})
    return render(request,'orders/admin.html',{"orders":orders})

def done(request,pk):
    """ Function to set orders to completed """
    order = get_object_or_404(Order,pk=pk)
    if request.method == 'POST':
        order.delivered_status = True
        order.save()
    pending = Order.objects.filter(payment_status=True,delivered_status=False)
    pending = Order.objects.filter(payment_status=True,delivered_status=False).all()
    orders = []
    for o in pending:
        orders.append({"order":o,"food":o.all_food()})
    return render(request,'orders/admin.html',{"orders":orders})
