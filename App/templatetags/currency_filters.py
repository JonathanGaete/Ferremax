from django import template
from App.utils import convertir_moneda

register = template.Library()

@register.filter(name='convertir_moneda')
def convertir_moneda_filter(precio, origen, destino):
    return convertir_moneda(origen, destino, precio)