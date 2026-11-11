import requests
from datetime import date, timedelta

from dao.dolar_dao import DolarDAO
from models.dolar import Dolar


class DolarService:
    APIS = (
        ("exchangerate-api", "https://api.exchangerate-api.com/v4/latest/USD", None),
        ("open-er-api", "https://open.er-api.com/v6/latest/USD", None),
        ("frankfurter", "https://api.frankfurter.app/latest", {"from": "USD", "to": "CLP"}),
        ("currency-api", "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json", None),
    )

    def __init__(self, dolar_dao: DolarDAO):
        self._dolar_dao = dolar_dao
        
    # typehint tipo de retorno: -> Dolar | None
    def obtener_cotizacion(self) -> Dolar | None:
        guardado = self._dolar_dao.obtener_ultima()
        # devolver el objeto ya guardado
        if guardado is not None and date.today() - guardado.timestamp < timedelta(days=1):
            return guardado

        # en cada vuelta. toma una api distinta
        # en orden. indice api que vale la primera 0

        """
                    ej de sintaxis

        for indice, valor in enumerate(lista):
            ...
        
                    en este caso el valor se desempaqueta en tres valores

        for i, (fuente, url, parametros) in enumerate(self.APIS):
            ...

        """
        for indice_api, (fuente, url, parametros) in enumerate(self.APIS):
            # la primera api se intenta hasta 6 veces
            # las dema solo 1 vez
            if indice_api == 0:
                cantidad_intentos = 6
            else:
                cantidad_intentos = 1

            for intento in range(cantidad_intentos):
                # la primera api, la recomendada
                if indice_api == 0:
                    # prueba 6 veces la primera api
                    # con timeout incremental 5 en 5 hasta 30 
                    # (6 veces totales)
                    timeout = 5 * (intento + 1)
                    # si los 6 intentos fallan, error de timeout
                # las demas apis, menos recomendadas
                else:
                    # prueba 1 vez las demás apis con un timeout de 5s
                    timeout = 5
                    # cuando pasan los 5s de timeout genera un error timeout

                try:
                    respuesta = requests.get(url, params=parametros, timeout=timeout)
                    if respuesta.status_code != 200:
                        #. si es 200. ni se da la molestia de intentar otra vez
                        # simplemente lo rompe
                        break
                    try:
                        datos = respuesta.json()
                    except ValueError:
                        # valor o formato no sirve: break
                        break
                    # TypeError: tipo de dato incorrecto
                    # ValueError: valor o formato invalido; OverflowError: numero fuera de rango para Python (convertir un timestamp muy grande).
                    try:
                        dolar = Dolar.limpiar_respuesta(fuente, datos)
                        # todos estos errores los capturamos
                        # desde el model dolar que intento limpiar
                    except (TypeError, ValueError, OverflowError):
                        break
                    self._dolar_dao.guardar(dolar)
                    return dolar

                # errores de solicitud HTTP
                except requests.exceptions.Timeout:
                    continue
                except requests.exceptions.ConnectionError:
                    break
                except requests.exceptions.RequestException:
                    break
        # aqui si todas las apis fallan, devuelve None
        # los try except prueban todas las apis 
        # puede devolver el guardado de la DB
        return guardado
    
