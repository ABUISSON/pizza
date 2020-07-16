from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from orders.models import Order
# Create your views here.

def index(request):
  if not request.user.is_authenticated:
      return render(request, "users/login.html", {"message": None})
  context = {
      "user": request.user
  }
  return render(request, "users/user.html", context)

def login_view(request):
  username = request.POST["username"]
  password = request.POST["password"]
  user = authenticate(request, username=username, password=password)
  if user is not None:
      login(request, user)
      if 'order_id' in request.session:
          Order.objects.filter(client=user, payment_status=False).delete() # Deleting existing pending order for user
          pk = request.session['order_id']
          order = Order.objects.get(pk=pk)
          order.client = request.user
          order.save()

          if 'order_finished' in request.session:
              return HttpResponseRedirect("cart")
      return HttpResponseRedirect(reverse("index"))
  else:
      return render(request, "users/login.html", {"message": "Invalid credentials."})

def logout_view(request):
  logout(request)
  return render(request, "users/login.html", {"message": "Logged out."})
