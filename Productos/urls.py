from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import * 

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'destacados', DestacadosViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
