# En mindicador_integration/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('moneda/', views.home, name='home'),
    # Otras URLs de la aplicación si es necesario
]
