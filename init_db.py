from orders.models import Topping, PizzaPrice, Sub_addon, Sub_main, Pasta, Salad, Plate

############
## Pizza ###
############

toppings = ['Pepperoni','Sausage','Mushrooms','Onions','Ham','Canadian Bacon','Pineapple','Eggplant','Tomato & Basil', 'Green Peppers','Hamburger','Spinach','Artichoke','Buffalo Chicken','Barvecue Chicken','Anchovies','Black Olives','Fresh Garlic','Zucchini']
for t in toppings:
    a = Topping(type=t)
    a.save()

prices_list = [('R','S',0,12.70),('R','S',1,13.70),('R','S',2,15.20),('R','S',3,16.20),('R','S',4,17.75),('R','L',0,17.95),('R','L',1,19.95),('R','L',2,21.95),('R','L',3,23.95),('R','L',4,25.95),('S','S',0,24.45),('S','S',1,26.45),('S','S',2,28.45),('S','S',3,29.45),('S','S',4,30.45),('S','L',0,38.70),('S','L',1,40.70),('S','L',2,42.70),('S','L',3,44.7),('S','L',4,45.70)]

for e in prices_list:
    type, size, n_tops, price = e
    a = PizzaPrice(pizza_type=type,pizza_size=size,n_tops=n_tops,price=price)
    a.save()

# ############
# ## SUBS ###
# ############

addons_list=['Mushrooms', 'Green Peppers', 'Onions', 'Extra Cheese']
for type in addons_list:
    a = Sub_addon(type=type, price=0.5)
    a.save()

subs = [("Cheese",6.50,7.95),("Italian",6.50,7.95),("Ham + Cheese",6.50,7.95),("Meatball",6.50,7.95),("Tuna",6.50,7.95),("Turkey",7.50,8.50),("Chicken Parmigiana",7.50,8.50),("Eggplant Parmigiana",6.50,7.95),("Steak",6.50,7.95),("Steak + Cheese",6.95,8.50),("Sausage, Peppers & Onions",0,8.50),("Hamburger",4.60,6.95),("Cheeseburger",5.10,7.45),("Fried Chicken",6.95,8.50),("Veggie",6.95,8.50)]

for sub in subs:
    name, price_s, price_l = sub
    a = Sub_main(name=name,price_s=price_s,price_l=price_l)
    a.save()

############
## PASTA ###
############

PASTAS={
"Baked Ziti w/Mozzarella":6.5,
"Baked Ziti w/Meatballs":8.75,
"Baked Ziti w/Chicken":9.75
}

for type in PASTAS.keys():
    a = Pasta(type=type, price=PASTAS[type])
    a.save()

############
## SALADS ###
############

SALADS = {
"Garden Salad":6.25,
"Greek Salad":8.25,
"Antipasto":8.25,
"Salad w/Tuna":8.25
}

for type in SALADS.keys():
    a = Salad(type=type, price=SALADS[type])
    a.save()

############
## PLATES ##
############


plate_info = [('Garden Salad','S', 40.00), ('Garden Salad','L', 65.00),
                ('Greek Salad', 'S', 50.00), ('Greek Salad', 'L', 75.00),
                ('Antipasto', 'S', 50.00), ('Antipasto', 'L', 75.00),
                ('Baked Ziti', 'S', 40.00), ('Baked Ziti', 'L', 65.00),
                ('Meatball Parm', 'S', 50.00), ('Meatball Parm', 'L', 75.00),
                ('Chicken Parm', 'S', 55.00), ('Chicken Parm', 'L', 85.00)]

for plate_type, plate_size, plate_price in plate_info:
    p = Plate(type=plate_type, size=plate_size, price=plate_price)
    p.save()
