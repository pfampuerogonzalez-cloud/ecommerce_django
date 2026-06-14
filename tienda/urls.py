from django.urls import path
from . import views

#EL REQUEST LLEGA DESDE EL ROUTER ACA Y CADA RUTA GATILLA UNA FUNCIÓN.
urlpatterns= [
    path ("productos/", views.lista_productos,),
    path ("borrar/pk:id/", views.lista_productos,),
]



