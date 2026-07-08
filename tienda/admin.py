from django.contrib import admin
from .models import Producto, ProductoPremium, Pedido, ItemPedido

class ProductoAdmin(admin.ModelAdmin):
    pass

class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'total', 'creado']
    list_filter = ['creado']

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['producto', 'cantidad', 'precio']

admin.site.register(Producto, ProductoAdmin)
admin.site.register(ProductoPremium)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido)
