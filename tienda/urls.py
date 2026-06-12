from django.urls import path
from . import views

urlpatterns= [
    path ("productos/", views.lista_productos,),
    path ("borrar/pk:id/", views.lista_productos,),
]



