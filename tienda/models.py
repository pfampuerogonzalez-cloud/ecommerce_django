from django.db import models

# Create your models here.

class Producto(models.Model):
    nombre = models.CharField(max_length=30)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to="productos/", blank=True,null=True)
    descripcion = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.nombre