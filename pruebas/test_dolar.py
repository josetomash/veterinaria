import os
import sys
import tempfile
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests

from dao.dolar_dao import DolarDAO
from database import ConexionDB
from models.dolar import Dolar
from services.dolar_service import DolarService


class RespuestaAPI:
    def __init__(self, status_code, datos=None):
        self.status_code = status_code
        self._datos = datos

    def json(self):
        return self._datos


def verificar(condicion, mensaje):
    if not condicion:
        raise RuntimeError(f"Prueba fallida: {mensaje}")


def test_normaliza_respuesta_principal():
    dolar = Dolar.limpiar_respuesta(
        "exchangerate-api",
        {"base": "USD", "date": "2026-11-11", "rates": {"CLP": 950.5}},
    )

    verificar(dolar.timestamp == date(2026, 11, 11), f"Fecha esperada 2026-11-11, obtuvo {dolar.timestamp}")
    verificar(dolar.valor_dolar == 1.0, f"Valor dolar esperado 1.0, obtuvo {dolar.valor_dolar}")
    verificar(dolar.conversion_clp == 950.5, f"CLP esperado 950.5, obtuvo {dolar.conversion_clp}")


def test_reintenta_con_timeout_creciente_y_guarda_fallback():
    timeouts_usados = []
    intentos = 0

    def get_falso(url, params=None, timeout=None):
        nonlocal intentos
        timeouts_usados.append(timeout)
        intentos += 1

        if intentos <= 6:
            raise requests.exceptions.Timeout()

        return RespuestaAPI(
            200,
            {
                "base_code": "USD",
                "time_last_update_unix": 1794355200,
                "rates": {"CLP": 951.25},
            },
        )

    get_original = requests.get
    try:
        requests.get = get_falso
        with tempfile.TemporaryDirectory() as carpeta_temp:
            ruta_db = os.path.join(carpeta_temp, "prueba.db")
            dao = DolarDAO(ConexionDB(ruta_db))
            servicio = DolarService(dao)

            dolar = servicio.obtener_cotizacion()

            verificar(isinstance(dolar, Dolar), "No devolvió una instancia de Dolar")
            verificar(dolar.conversion_clp == 951.25, f"CLP esperado 951.25, obtuvo {dolar.conversion_clp}")
            verificar(
                timeouts_usados == [5, 10, 15, 20, 25, 30, 5],
                f"Timeouts incorrectos: {timeouts_usados}",
            )
            ultima = dao.obtener_ultima()
            verificar(
                ultima is not None and ultima.conversion_clp == 951.25,
                "No se guardó correctamente el fallback en la base de datos",
            )

            print(f"\nDB temporal creada en: {carpeta_temp}")
            input("Pausado para revisar en Finder. Presiona Enter para borrarla y continuar...")
    finally:
        requests.get = get_original


def test_reutiliza_cotizacion_guardada_durante_el_dia():
    llamadas_api = 0

    def get_falso(url, params=None, timeout=None):
        nonlocal llamadas_api
        llamadas_api += 1

    get_original = requests.get
    try:
        requests.get = get_falso
        with tempfile.TemporaryDirectory() as carpeta_temp:
            ruta_db = os.path.join(carpeta_temp, "prueba.db")
            dao = DolarDAO(ConexionDB(ruta_db))
            servicio = DolarService(dao)

            dao.guardar(Dolar(date.today(), 1, 950))
            dolar = servicio.obtener_cotizacion()

            verificar(dolar is not None and dolar.conversion_clp == 950, "No reutilizó el valor guardado de 950")
            verificar(llamadas_api == 0, f"Se esperaba 0 llamadas a la API, pero hubo {llamadas_api}")
    finally:
        requests.get = get_original


if __name__ == "__main__":
    test_normaliza_respuesta_principal()
    test_reintenta_con_timeout_creciente_y_guarda_fallback()
    test_reutiliza_cotizacion_guardada_durante_el_dia()
    print("Todas las pruebas pasaron correctamente.")