import sqlite3

from dao import DetalleConsultaDAO
from models import DetalleConsulta


class DetalleConsultaService:
    def __init__(self, detalle_consulta_dao: DetalleConsultaDAO):
        self._detalle_consulta_dao = detalle_consulta_dao

    def registrar_detalle_consulta(self, detalle: DetalleConsulta) -> DetalleConsulta:
        if not isinstance(detalle, DetalleConsulta):
            raise TypeError("Debe proporcionar un detalle de consulta válido.")
        try:
            self._detalle_consulta_dao.insertar(detalle)
            return detalle
        except sqlite3.IntegrityError as error:
            raise ValueError(f"No se pudo registrar el detalle de consulta: {error}") from error
