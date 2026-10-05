import sqlite3

from dao import ConsultaDAO
from models import Consulta


class ConsultaService:
    def __init__(self, consulta_dao: ConsultaDAO):
        self._consulta_dao = consulta_dao

    def registrar_consulta(self, consulta: Consulta) -> Consulta:
        if not isinstance(consulta, Consulta):
            raise TypeError("Debe proporcionar una consulta válida.")
        try:
            self._consulta_dao.insertar(consulta)
            return consulta
        except sqlite3.IntegrityError as error:
            raise ValueError(f"No se pudo registrar la consulta: {error}") from error
