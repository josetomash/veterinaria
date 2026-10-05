import sqlite3

from dao import EspecieDAO
from models import Especie


class EspecieService:
    def __init__(self, especie_dao: EspecieDAO):
        self._especie_dao = especie_dao

    def registrar_especie(self, especie: Especie) -> Especie:
        if not isinstance(especie, Especie):
            raise TypeError("Debe proporcionar una especie válida.")
        try:
            self._especie_dao.insertar(especie)
            return especie
        except sqlite3.IntegrityError as error:
            nombre_limpio = especie.nombre.strip()
            raise ValueError(f"No se pudo registrar: la especie '{nombre_limpio}' ya existe en el sistema.") from error
