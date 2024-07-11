import requests
from django.conf import settings

def convertir_moneda(origen, destino, cantidad):
    url = f"{settings.MINDICADOR_API_URL}/{origen}/{destino}"
    params = {
        'apikey': settings.MINDICADOR_API_KEY,
        'cantidad': cantidad
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        monto_convertido = data['cantidad']
        return monto_convertido
    else:
        # Manejo de errores
        return None
