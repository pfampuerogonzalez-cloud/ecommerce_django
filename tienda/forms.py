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

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")
        return precio

class ProductoPremiumForms(forms.ModelForm):

    class Meta:
        model = ProductoPremium
        fields = [
            "nombre",
            "precio",
            "imagen",
            "descripcion"
        ]

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")
        return precio  