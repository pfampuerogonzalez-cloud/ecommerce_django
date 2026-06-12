from django.shortcuts import render
from django.http import HttpResponse
from .models import Producto

# Create your views here.

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, "productos.html",{"productos":productos})

def borrar_productos(request):
    productos = Producto.objects.get(id=10)
    productos.delete()

def actualizar_productos(request):
    pass

def crear_productos(request):
    pass