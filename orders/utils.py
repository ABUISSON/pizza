def compute_price(order):
    price = 0
    for pizza in order.pizzas.all():
        price+=pizza_price(pizza)
    return price

#à mettre dans la db
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


def pizza_price(pizza):
    k = min(4,len(pizza.toppings.all()))
    return PIZZA_PRICES[pizza.pizza_type][pizza.pizza_size][k]

def get_unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
