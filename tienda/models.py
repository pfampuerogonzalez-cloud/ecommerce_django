from django.db import models
from django.conf import settings

class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to="productos/", blank=True,null=True)
    descripcion = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.nombre

class ProductoPremium(models.Model):
    nombre = models.CharField(max_length=30)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to="premium/", blank=True,null=True)
    descripcion = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.nombre

class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedidos')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    total = models.IntegerField(default=0)

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return f"Pedido #{self.id} - {self.usuario.username}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.IntegerField()

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

    @property
    def subtotal(self):
        return self.precio * self.cantidad