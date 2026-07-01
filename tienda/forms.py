from django import forms
from .models import Producto, ProductoPremium

class ProductoForms(forms.ModelForm):

    class Meta:
        model = Producto
        fields= ["nombre",
                 "precio",
                 "imagen",
                 "descripcion"
                 ]
        

class ProductoPremiumForms(forms.ModelForm):

    class Meta:
        model = ProductoPremium
        fields = [
            "nombre",
            "precio",
            "imagen",
            "descripcion"
        ]  