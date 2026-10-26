import os
from dotenv import load_dotenv

# Carga las variables declaradas en el archivo .env a la memoria del sistema operativo
load_dotenv()

class Configuracion:

    # Lectura tipada y con valores por defecto razonables
    API_KEY_CLIMA: str = os.getenv("WEATHER_API_KEY", "")
    URL_BASE_CLIMA: str = os.getenv("WEATHER_BASE_URL", "https://api.weatherapi.com/v1")
    CIUDAD_CLINICA: str = os.getenv("CIUDAD_DEFECTO_CLINICA", "Nacimiento")
    TIMEOUT: int = int(os.getenv("TIMEOUT_SEGUNDOS", "5"))

    @classmethod
    def validar_secretos_criticos(cls):

        # Valida que la clave meteorológica exista antes de realizar consultas de red.
        # Aplica el principio Fail Fast para alertar al programador de inmediato.
        
        if not cls.API_KEY_CLIMA or cls.API_KEY_CLIMA.startswith("tu_api_key"):
            raise ValueError(
                "[ERROR CRÍTICO DE SEGURIDAD] La variable 'WEATHER_API_KEY' no está configurada "
                "correctamente en el archivo local .env. Registra tu clave gratuita en WeatherAPI.com."
            )
