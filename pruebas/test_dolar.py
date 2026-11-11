import os
import tempfile
import unittest
from datetime import date
from unittest.mock import patch

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


class TestDolar(unittest.TestCase):
    def setUp(self):
        self.directorio_temporal = tempfile.TemporaryDirectory()
        ruta_db = os.path.join(self.directorio_temporal.name, "prueba.db")
        self.dao = DolarDAO(ConexionDB(ruta_db))
        self.servicio = DolarService(self.dao)

    def tearDown(self):
        self.directorio_temporal.cleanup()

    def test_normaliza_respuesta_principal_a_objeto_dominio(self):
        dolar = Dolar.limpiar_respuesta(
            "exchangerate-api",
            {"base": "USD", "date": "2026-11-11", "rates": {"CLP": 950.5}},
        )

        self.assertEqual(dolar.timestamp, date(2026, 11, 11))
        self.assertEqual(dolar.valor_dolar, 1.0)
        self.assertEqual(dolar.conversion_clp, 950.5)

    @patch("services.dolar_service.requests.get")
    def test_reintenta_con_timeout_creciente_y_guarda_el_fallback(self, get):
        get.side_effect = [
            requests.exceptions.Timeout()
            for _ in range(6)
        ] + [
            RespuestaAPI(
                200,
                {
                    "base_code": "USD",
                    "time_last_update_unix": 1794355200,
                    "rates": {"CLP": 951.25},
                },
            )
        ]

        dolar = self.servicio.obtener_cotizacion()

        self.assertIsInstance(dolar, Dolar)
        self.assertEqual(dolar.conversion_clp, 951.25)
        self.assertEqual(
            [llamada.kwargs["timeout"] for llamada in get.call_args_list],
            [5, 10, 15, 20, 25, 30, 5],
        )
        self.assertEqual(self.dao.obtener_ultima().conversion_clp, 951.25)

    @patch("services.dolar_service.requests.get")
    def test_reutiliza_cotizacion_guardada_durante_el_dia(self, get):
        self.dao.guardar(Dolar(date.today(), 1, 950))

        dolar = self.servicio.obtener_cotizacion()

        self.assertEqual(dolar.conversion_clp, 950)
        get.assert_not_called()


if __name__ == "__main__":
    unittest.main()