def carrito_cantidad(request):
    cart = request.session.get('cart', {})
    cantidad = sum(cart.values())
    return {'carrito_cantidad': cantidad}
