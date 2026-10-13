import sqlite3

from dao import PropietarioDAO
from models import Propietario

class PropietarioService:
    def __init__(self, propietario_dao: PropietarioDAO):
        self._propietario_dao = propietario_dao

    def obtener_propietario_por_id(self, id_propietario: int) -> Propietario:
        return self._propietario_dao.obtener_por_id_estricto(id_propietario)

    def listar_propietarios(self) -> list[Propietario]:
        return self._propietario_dao.listar_todos()

    def buscar_propietarios_por_nombre(self, termino: str) -> list[Propietario]:
        termino_limpio = termino.strip().casefold()
        if not termino_limpio:
            raise ValueError("Debe proporcionar un nombre para buscar.")
        return [
            propietario
            for propietario in self._propietario_dao.listar_todos()
            if termino_limpio in propietario.nombre.casefold()
        ]
    
    def registrar_propietario(self, propietario: Propietario) -> Propietario:
        if not isinstance(propietario, Propietario):
            raise TypeError("Debe proporcionar un propietario válido.")
        try:
            self._propietario_dao.insertar(propietario)
            return propietario
        except sqlite3.IntegrityError as error:
            nombre_limpio = propietario.nombre.strip()
            raise ValueError(f"No se pudo registrar: el propietario '{nombre_limpio}' ya existe en el sistema.") from error

    def actualizar_propietario(self, propietario: Propietario) -> bool:
        return self._propietario_dao.actualizar(propietario)

    def borrar_propietario(self, id_propietario: int) -> bool:
        return self._propietario_dao.eliminar(id_propietario)