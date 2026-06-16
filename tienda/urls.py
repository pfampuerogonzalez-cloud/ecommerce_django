from django.urls import path
from . import views

#EL REQUEST LLEGA DESDE EL ROUTER ACA Y CADA RUTA GATILLA UNA FUNCIÓN.
urlpatterns= [
    path ("productos/", views.lista_productos, name="lista_productos"),
    path ("crear", views.crear_productos, name="crear_producto"),
]



