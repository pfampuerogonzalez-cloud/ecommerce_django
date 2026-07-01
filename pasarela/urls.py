from django.urls import path
from . import views

#EL REQUEST LLEGA DESDE EL ROUTER ACA Y CADA RUTA GATILLA UNA FUNCIÓN.
urlpatterns= [
    path ("pago/", views.mercadolibre,),
]