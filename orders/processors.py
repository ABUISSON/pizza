from .models import Order

def get_cart_size(request):
    n_cart=0
    if request.user.is_authenticated:
        if Order.objects.filter(client=request.user,payment_status=False).count()>0:
            o = Order.objects.get(client=request.user,payment_status=False) #TODO: tester que tout se passe bien
            cart_isfull = True
            n_cart = o.get_order_size()
        else:
            cart_isfull = False
    else:
        if 'order_id' in request.session:
            cart_isfull = True
            o = Order.objects.get(pk=request.session['order_id'])
            n_cart = o.get_order_size()
        else:
            cart_isfull = False
    return {"cart_isfull":cart_isfull,"n_cart":n_cart}
