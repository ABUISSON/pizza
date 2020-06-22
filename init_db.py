from orders.models import PizzaPrice, Sub_addon, Sub, Pasta, Salad, Plate

#I added toppings manually

############
## SUBS ###
############

# addons_list=['Mushrooms', 'Green Peppers', 'Onions', 'Extra Cheese']
# for type in addons_list:
#     a = Sub_addon(type=type, price=0.5)
#     a.save()

sub_mains=["Cheese","Italian","Ham + Cheese","Meatball","Tuna","Turkey","Chicken Parmigiana","Eggplant Parmigiana","Steak","Steak + Cheese","Sausage, Peppers & Onions","Hamburger","Cheeseburger","Fried Chicken","Veggie"]

for main in sub_mains:
    a = Sub(main=main, size='S')
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

plate_types = ["Garden Salad", "Greek Salad","Antipasto","Baked Ziti","Meatball Parm","Chicken Parm"]

for type in plate_types:
    p = Plate(type=type, size='S')
    p.save()
