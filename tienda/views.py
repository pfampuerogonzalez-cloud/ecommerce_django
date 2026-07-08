from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Producto, ProductoPremium, Pedido, ItemPedido
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
  


def borrar_premium(request, id):
    premium = ProductoPremium.objects.get(id=id)
    premium.delete()
    messages.success(request,"producto premium borrado correctamente")
    return redirect("lista_productos_premium")


# DETALLE DE PRODUCTO

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, "detalle_producto.html", {"producto": producto})


# CARRITO DE COMPRAS (sesión)

def ver_carrito(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for producto_id, cantidad in cart.items():
        producto = get_object_or_404(Producto, id=producto_id)
        subtotal = producto.precio * cantidad
        total += subtotal
        items.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})
    return render(request, "carrito.html", {"items": items, "total": total})


def agregar_al_carrito(request, producto_id):
    cart = request.session.get('cart', {})
    pid = str(producto_id)
    if pid in cart:
        cart[pid] += 1
    else:
        cart[pid] = 1
    request.session['cart'] = cart
    messages.success(request, "Producto agregado al carrito.")
    return redirect("ver_carrito")


def quitar_del_carrito(request, producto_id):
    cart = request.session.get('cart', {})
    pid = str(producto_id)
    cart.pop(pid, None)
    request.session['cart'] = cart
    messages.success(request, "Producto quitado del carrito.")
    return redirect("ver_carrito")


def actualizar_cantidad(request, producto_id):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        pid = str(producto_id)
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad > 0:
            cart[pid] = cantidad
        else:
            cart.pop(pid, None)
        request.session['cart'] = cart
    return redirect("ver_carrito")


# CHECKOUT Y PEDIDOS

@login_required
def confirmar_pedido(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect("ver_carrito")

    if request.method == "POST":
        pedido = Pedido.objects.create(usuario=request.user, total=0)
        total = 0
        for producto_id, cantidad in cart.items():
            producto = get_object_or_404(Producto, id=producto_id)
            precio = producto.precio
            ItemPedido.objects.create(
                pedido=pedido, producto=producto,
                cantidad=cantidad, precio=precio
            )
            total += precio * cantidad
        pedido.total = total
        pedido.save()
        del request.session['cart']
        messages.success(request, "¡Pedido confirmado exitosamente!")
        return redirect("detalle_pedido", pedido.id)

    items = []
    total = 0
    for producto_id, cantidad in cart.items():
        producto = get_object_or_404(Producto, id=producto_id)
        subtotal = producto.precio * cantidad
        total += subtotal
        items.append({'producto': producto, 'cantidad': cantidad, 'subtotal': subtotal})
    return render(request, "confirmar_pedido.html", {"items": items, "total": total})


@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, "detalle_pedido.html", {"pedido": pedido})


@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, "mis_pedidos.html", {"pedidos": pedidos})
