from django.urls import path
from . import views

#EL REQUEST LLEGA DESDE EL ROUTER ACA Y CADA RUTA GATILLA UNA FUNCIÓN.
urlpatterns= [
    path ("", views.index, name="index"),
    path ("crear/", views.crear_producto, name="crear_producto"),
    path ("productos/", views.lista_productos, name="lista_productos"),
    path ("actualizar/<int:id>/", views.actualizar_producto, name="actualizar_producto"),
    path ("borrar/<int:id>/", views.borrar_producto, name="borrar_producto"),

]



