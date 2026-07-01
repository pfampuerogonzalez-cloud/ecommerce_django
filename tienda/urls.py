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
    path("actualizar_premium/<int:id>/",views.actualizar_producto, name="actualizar_producto"),
    path("borrar_premium/<int:id>/",views.borrar_premium, name="borrar_producto_premium"),

]



