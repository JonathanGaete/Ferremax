from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone



class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre



class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    categoria = models.ForeignKey('Categoria', related_name='productos', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', default='productos')
    
    def __str__(self):
        return self.nombre



class Destacados(models.Model):
    nombre = models.CharField(max_length=50)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    

