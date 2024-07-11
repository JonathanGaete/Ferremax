import requests

def get_indicators():
    url = "https://mindicador.cl/api"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
