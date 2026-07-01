from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Producto, ProductoPremium
from .forms import ProductoForms, ProductoPremiumForms
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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


# CRUD PREMIUM

#C (CREATE)
def crear_premium(request):
    # SI EL REQUEST LLEGA POR METODO POST PASA ALGO
    if request.method == "POST":
        #LLEGA EN REQUEST CON LOS DATOS DESDE EL NAVEGADOR Y SE CARGAN EN EL FORMULARIO
        form = ProductoPremiumForms(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("lista_productos_premium")
    #DE LO CONTRARIO SE ENTREGA EL FORMULARIO VACIO
    else:
        form = ProductoPremiumForms()
    
    return render(request,"premium/formulario_premium.html",{"form":form})


# READ DEL CRUD
def lista_productos_premium(request):
    productosPremium = ProductoPremium.objects.all()
    return render(request, "premium/lista_premium.html", {"premium": productosPremium})

def actualizar_premium(request, id):
     
    premium = ProductoPremium.objects.get(id=id)

    if request.method == "POST":
        form = ProductoPremiumForms(request.POST,request.FILES, instance=premium)
        
        if form.is_valid():
            form.save()
            messages.success(request,"producto premium actualizado correctamente")
            return redirect("lista_productos")
    else:
        form = ProductoPremiumForms(instance=premium)
       

    return render(request, "actualizar_productos_premium.html",{"form":form})
  


def borrar_premium(request):
    premium = ProductoPremium.objects.get(id=id)
    premium.delete()
    messages.success(request,"producto premium borrado correctamente")
    return redirect("lista_productos_premium")



