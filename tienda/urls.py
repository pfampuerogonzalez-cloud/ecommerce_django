from django.urls import path
from . import views

#EL REQUEST LLEGA DESDE EL ROUTER ACA Y CADA RUTA GATILLA UNA FUNCIÓN.
urlpatterns= [
    path ("", views.index, name="index"),
    path ("crear/", views.crear_producto, name="crear_producto"),
    path ("productos/", views.lista_productos, name="lista_productos"),
    path ("actualizar/<int:id>/", views.actualizar_producto, name="actualizar_producto"),
    path ("borrar/<int:id>/", views.borrar_producto, name="borrar_producto"),
    path ("lista_premium/", views.lista_productos_premium, name="lista_productos_premium"),
    path ("crear_premium/", views.crear_premium, name="crear_premium"),
    path("actualizar_premium/<int:id>/",views.actualizar_premium, name="actualizar_premium"),
    path("borrar_premium/<int:id>/",views.borrar_premium, name="borrar_producto_premium"),

    # Detalle de producto
    path("producto/<int:id>/", views.detalle_producto, name="detalle_producto"),

    # Carrito
    path("carrito/", views.ver_carrito, name="ver_carrito"),
    path("carrito/agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar_al_carrito"),
    path("carrito/quitar/<int:producto_id>/", views.quitar_del_carrito, name="quitar_del_carrito"),
    path("carrito/actualizar/<int:producto_id>/", views.actualizar_cantidad, name="actualizar_cantidad"),

    # Checkout y pedidos
    path("carrito/confirmar/", views.confirmar_pedido, name="confirmar_pedido"),
    path("pedido/<int:pedido_id>/", views.detalle_pedido, name="detalle_pedido"),
    path("mis-pedidos/", views.mis_pedidos, name="mis_pedidos"),

]



