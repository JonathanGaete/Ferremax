from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from Productos.models import *
from django.views.generic.base import View

class Banner(models.Model):
    nombre = models.CharField(max_length=50)
    imagen = models.ImageField(upload_to="Banner", null=True)

    def __str__(self):
        return self.nombre

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    TIPO_USUARIO = (
        ('bodeguero', 'Bodeguero'),
        ('cliente', 'Cliente'),
        ('admin', 'Admin'),
    )
    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO, default='cliente')

    # Ajusta related_name para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='groups',
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.nombre}'

    def get_total_price(self):
        return self.quantity * self.product.precio

class Pedido(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, default='pendiente')  # Opcional: para el estado del pedido

class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    cart_item = models.OneToOneField(CartItem, on_delete=models.CASCADE, null=True, blank=True)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
