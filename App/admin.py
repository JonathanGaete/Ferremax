from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Banner)
admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(CustomUser)
admin.site.register(Pedido)
admin.site.register(PedidoItem)
admin.site.register(Cart)
admin.site.register(CartItem) 