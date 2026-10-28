# import request la libreria para API REST
import requests

class DolarMenu:
    def __init__(self, clp):
        # url de la api
        self.api_url = "https://api.exchangerate-api.com/v4/latest/USD"
    # currency code es el valor ISO de la moneda (CLP)
    def get_exchange_rate(self, currency_code):
        try:
            # Hacer la solicitud al endpoint de la API para obtener la tasa de cambio
            response = requests.get(self.api_url)
            # Verificar si la solicitud fue exitosa
            response.raise_for_status()
            # parsear la respuesta JSON que entrego el servidor en una variable llamada data
            data = response.json()
            # get intenta buscar la clave de forma segura
            informacion = [
                        'valor':data['rates'].get(currency_code, None),
                        'fecha':data.get(date, None)
                    ]
            return informacion
        # tira una excepcion si la solicitud falla, siendo más especifico, una RequestException
        except requests.exceptions.RequestException as e:
            # este except no se activa si tiras un valor ISO que no existe.
            print(f"Error en status de la respuesta: {e}")
            return None
