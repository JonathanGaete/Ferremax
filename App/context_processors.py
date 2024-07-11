
import requests
from django.conf import settings

def mindicador_api(request):
    # URL de la API de Mindicador
    api_url = 'https://mindicador.cl/api'

    try:
        # Realizar la solicitud GET a la API de Mindicador
        response = requests.get(api_url)
        data = response.json()  # Convertir la respuesta a JSON

        # Extraer los indicadores que deseas utilizar
        indicadores = data['serie']

        # Formatear los datos según sea necesario
        contexto_mindicador = {
            'indicadores_mindicador': indicadores,
            # Puedes añadir más datos de contexto según necesites
        }

    except requests.exceptions.RequestException as e:
        # Manejar errores de conexión con la API
        print(f"Error al conectar con la API de Mindicador: {e}")
        contexto_mindicador = {}

    return contexto_mindicador
