import requests
from typing import Optional
from config.configuracion import Configuracion
from models.pronostico import Pronostico

class ServicioClima:
    
    # Cliente seguro para comunicarse con la API de WeatherAPI.com inyectando credenciales desde el entorno seguro.
    
    @classmethod
    def consultar_clima_comuna(cls, nombre_comuna: str) -> Optional[Pronostico]:
        
        # Consulta las condiciones climáticas de una comuna o ciudad. Retorna una instancia de Pronostico o None ante errores de red o autenticación.
        # Fail Fast: Validar presencia de credenciales en memoria
        
        Configuracion.validar_secretos_criticos()

        endpoint = f"{Configuracion.URL_BASE_CLIMA}/current.json"
        parametros = {
            "key": Configuracion.API_KEY_CLIMA,
            "q": nombre_comuna.strip(),
            "lang": "es"
        }

        try:
            respuesta = requests.get(
                endpoint,
                params=parametros,
                timeout=Configuracion.TIMEOUT
            )

            if respuesta.status_code == 200:
                datos = respuesta.json()
                ubicacion = datos.get("location", {})
                actual = datos.get("current", {})
                condicion = actual.get("condition", {}).get("text", "Desconocido")

                return Pronostico(
                    ciudad=ubicacion.get("name", nombre_comuna),
                    region=ubicacion.get("region", ""),
                    temperatura_c=actual.get("temp_c", 0.0),
                    condicion=condicion,
                    humedad=actual.get("humidity", 0)
                )

            elif respuesta.status_code in (401, 403):
                print(f"[SEGURIDAD ALERTA] API Key rechazada por WeatherAPI (HTTP {respuesta.status_code}). Verifica tu archivo .env.")
                return None
            elif respuesta.status_code == 400:
                print(f"[CLIMA AVISO] No se encontró información meteorológica para la comuna '{nombre_comuna}'.")
                return None
            else:
                print(f"[CLIMA ERROR] Respuesta inesperada del servidor (HTTP {respuesta.status_code}).")
                return None

        except requests.exceptions.Timeout:
            print("[CLIMA TIMEOUT] Tiempo de espera agotado al consultar el clima.")
            return None
        except requests.exceptions.ConnectionError:
            print("[CLIMA RED] No hay conexión disponible para consultar el servicio meteorológico.")
            return None
