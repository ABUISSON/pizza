from orders.models import PizzaPrice

PIZZA_PRICES = {
"R":{
    "S":{0:12.7,1:13.7,2:15.2,3:16.2,4:17.75},
    "L":{0:17.95,1:19.95,2:21.95,3:23.95,4:25.95}
    },
"S":{
    "S":{0:24.45,1:26.45,2:28.45,3:29.45,4:30.45},
    "L":{0:38.7,1:40.7,2:42.7,3:44.7,4:45.7}
    }
}

for type in PIZZA_PRICES.keys():
  for size in PIZZA_PRICES[type].keys():
    for n_tops in PIZZA_PRICES[type][size]:
          p = PizzaPrice(pizza_type=type,pizza_size=size,n_tops=n_tops,price=PIZZA_PRICES[type][size][n_tops])
          p.save()
