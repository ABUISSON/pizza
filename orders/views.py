from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render

from .utils import compute_price, get_unique
from .forms import OrderForm
from .models import Topping, Pizza, Order, Pasta, Salad, Sub, Sub_main, Sub_addon

def index(request):
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
    order, created = Order.objects.get_or_create(client=request.user,payment_status=False)
    context = {"Pizza": [str(e) for e in order.pizzas.all()],
    "price": compute_price(order)}
    return render(request, "orders/cart.html", context)

def pay(request):
    """This function takes to payment page"""
    context = {"price":request.GET.get('price')}
    return render(request, "orders/payment.html", context)

def get_order(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = OrderForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            pizza = Pizza.objects.create(pizza_type=form.cleaned_data['pizza_type'],pizza_size=form.cleaned_data['pizza_size'])
            for top in form.cleaned_data['toppings']:
                    top_obj, created = Topping.objects.get_or_create(type=top)
                    pizza.toppings.add(top_obj)
            pizza.save()

            #add to order or create
            order, created = Order.objects.get_or_create(client=request.user,payment_status=False)
            order.pizzas.add(pizza)
            # redirect to a new URL:
            return HttpResponseRedirect('cart')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = OrderForm()

    return render(request, 'orders/order.html', {'form': form})


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
