import sqlite3

from dao import EspecialidadDAO
from models import Especialidad


class EspecialidadService:
    def __init__(self, especialidad_dao: EspecialidadDAO):
        self._especialidad_dao = especialidad_dao

    def registrar_especialidad(self, especialidad: Especialidad) -> Especialidad:
        if not isinstance(especialidad, Especialidad):
            raise TypeError("Debe proporcionar una especialidad válida del Enum Especialidad.")
        try:
            self._especialidad_dao.insertar(especialidad)
            return especialidad
        except sqlite3.IntegrityError as error:
            nombre_limpio = especialidad.value.strip()
            raise ValueError(f"No se pudo registrar: la especialidad '{nombre_limpio}' ya existe en el sistema.") from error
