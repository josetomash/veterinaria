import sqlite3

from dao import PropietarioDAO
from models import Propietario

class PropietarioService:
    def __init__(self, propietario_dao: PropietarioDAO):
        self._propietario_dao = propietario_dao
    
    def registrar_propietario(self, propietario: Propietario) -> Propietario:
        if not isinstance(propietario, Propietario):
            raise TypeError("Debe proporcionar un propietario válido.")
        try:
            self._propietario_dao.insertar(propietario)
            return propietario
        except sqlite3.IntegrityError as error:
            nombre_limpio = propietario.nombre.strip()
            raise ValueError(f"No se pudo registrar: el propietario '{nombre_limpio}' ya existe en el sistema.") from error