from django import forms
from .models import Topping

PIZZA_TYPES = (
('R','Regular'),
('S', 'Sicilian')
)

PIZZA_SIZES = (
('S','Small'),
('L','Large')
)

class OrderForm(forms.Form):
    pizza_type = forms.ChoiceField(choices = PIZZA_TYPES, label="Pizza Type")
    pizza_size = forms.ChoiceField(choices = PIZZA_SIZES, label="Pizza Size")
    toppings = forms.ModelMultipleChoiceField(queryset = Topping.objects.all(), widget=forms.CheckboxSelectMultiple, required=True)
