from django import forms
from .models import Topping, Salad, Pasta, Sub_main, Sub_addon

PIZZA_TYPES = (
('R','Regular'),
('S', 'Sicilian')
)

PIZZA_SIZES = (
('S','Small'),
('L','Large')
)

SUB_SIZES = (
('S','Small'),
('L','Large')
)

class PizzaForm(forms.Form):
    pizza_type = forms.ChoiceField(choices=PIZZA_TYPES, widget=forms.RadioSelect, label="Pizza Type")
    pizza_size = forms.ChoiceField(choices=PIZZA_SIZES, widget=forms.RadioSelect, label="Pizza Size")
    toppings = forms.ModelMultipleChoiceField(queryset = Topping.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

class SaladForm(forms.Form):
    salad_type = forms.ModelChoiceField(queryset=Salad.objects.all(),
                label="Salad Type")

class PastaForm(forms.Form):
    pasta_type = forms.ModelChoiceField(queryset=Pasta.objects.all(),
                label="Pasta Type")

class SubForm(forms.Form):
    sub_main = forms.ModelChoiceField(queryset=Sub_main.objects.all(),
                label="Sub Type")
    sub_size = forms.ChoiceField(choices=SUB_SIZES, widget=forms.RadioSelect, label="Sub Size")
    toppings = forms.ModelMultipleChoiceField(queryset = Sub_addon.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
