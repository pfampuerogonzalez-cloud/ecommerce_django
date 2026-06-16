from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto
from .forms import ProductoForms
from django.contrib import messages

# Create your views here.
#CRUD

#CREATE
def crear_productos(request):
    #SI EL USUARIO ENVIÓ EL FORMULARIO
    if request.method == "POST":
        form = ProductoForms(request.POST, request.FILES) #request.POST (SON TODOS LOS DATOS DEL FORMULARIO)

        if form.is_valid():
            form.save()
            messages.success(request, "Producto guardado correctamente.")
            return redirect("lista_productos")

    else:
        form = ProductoForms()

    return render(request, "crear_producto.html",{"form":form})

#READ (LECTURA DE DATOS)

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, "productos.html",{"productos":productos})

def borrar_productos(request):
    productos = Producto.objects.get(id=id)
    productos.delete()

def actualizar_productos(request):
    pass

