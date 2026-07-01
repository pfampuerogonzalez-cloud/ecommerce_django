from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto
from .forms import ProductoForms
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request,"index.html",{})
#CRUD

#CREATE
def crear_producto(request):
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

#UPDATE
def actualizar_producto(request, id):
    producto = Producto.objects.get(id=id)

    if request.method == "POST":
        form = ProductoForms(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "producto actualizado correctamente")
            return redirect("lista_productos")
    else:
        form = ProductoForms(instance=producto)

    return render(request, "actualizar_productos.html", {"form": form})

def borrar_producto(request, id):
    producto = Producto.objects.get(id=id)
    producto.delete()
    messages.success(request, "borrado correctamente!")
    return redirect("lista_productos")



