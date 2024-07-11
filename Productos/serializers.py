from rest_framework import serializers
from .models import *
from rest_framework.response import Response
from rest_framework.decorators import api_view


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class DestacadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destacados
        fields = '__all__'
        

@api_view(['GET'])
def lista_productos(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)       


