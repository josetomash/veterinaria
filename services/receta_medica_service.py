import sqlite3

from dao import RecetaMedicaDAO
from models import RecetaMedica


class RecetaMedicaService:
    def __init__(self, receta_medica_dao: RecetaMedicaDAO):
        self._receta_medica_dao = receta_medica_dao

    def registrar_receta_medica(self, receta: RecetaMedica) -> RecetaMedica:
        if not isinstance(receta, RecetaMedica):
            raise TypeError("Debe proporcionar una receta médica válida.")
        try:
            self._receta_medica_dao.insertar(receta)
            return receta
        except sqlite3.IntegrityError as error:
            nombre_limpio = receta.nombre_comercial.strip()
            raise ValueError(f"No se pudo registrar: la receta médica '{nombre_limpio}' ya existe en el sistema.") from error
