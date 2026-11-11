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

    def obtener_cotizacion(self) -> Dolar | None:
        guardado = self._dolar_dao.obtener_ultima()
        if guardado is not None and date.today() - guardado.timestamp < timedelta(days=1):
            return guardado

        for indice_api, (fuente, url, parametros) in enumerate(self.APIS):
            cantidad_intentos = 6 if indice_api == 0 else 1
            for intento in range(cantidad_intentos):
                timeout = 5 * (intento + 1) if indice_api == 0 else 5
                try:
                    respuesta = requests.get(url, params=parametros, timeout=timeout)
                    if respuesta.status_code != 200:
                        break
                    try:
                        datos = respuesta.json()
                    except ValueError:
                        break
                    try:
                        dolar = Dolar.limpiar_respuesta(fuente, datos)
                    except (KeyError, TypeError, ValueError, OverflowError):
                        break
                    self._dolar_dao.guardar(dolar)
                    return dolar
                except requests.exceptions.Timeout:
                    if indice_api > 0 or intento == cantidad_intentos - 1:
                        break
                except requests.exceptions.ConnectionError:
                    break
                except requests.exceptions.RequestException:
                    break

        return guardado
