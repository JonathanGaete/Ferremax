
from rest_framework import viewsets
from Productos.models import *
from .serializers import *
from .permissions import IsBodeguero
from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsBodeguero]  # Aplica el permiso personalizado
    search_fields = ['nombre', 'descripcion', 'categoria__nombre']

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsBodeguero]

def productos_view(request):
    # Obtener todos los productos para pasar al template
    productos = Producto.objects.all()
    context = {
        'productos': productos
    }
    return render(request, 'pagina/productos.html', context)

class DestacadosViewSet(viewsets.ModelViewSet):
    queryset = Destacados.objects.all()
    serializer_class = DestacadosSerializer
    permission_classes = [IsBodeguero]  # Aplica el permiso personalizado


@api_view(['GET'])
@permission_classes([AllowAny])
def lista_productos(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

