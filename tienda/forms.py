from django import forms
from .models import Producto

class ProductoForms(forms.ModelForm):

    class Meta:
        model = Producto
        fields= ["nombre"
                 "precio",
                 "imagen",
                 "descripcion"
                 ]

    #def clean_precio(self):
       # precio = self.cleaned_data["precio"]

       # if precio <= 0:
            #raise forms.ValidationError("El precio debe ser mayor a 0")
        
        #return precio