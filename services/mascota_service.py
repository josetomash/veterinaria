import sqlite3

from dao import MascotaDAO
from models import Mascota


class MascotaService:
    def __init__(self, mascota_dao: MascotaDAO):
        self._mascota_dao = mascota_dao

    def obtener_mascota_por_id(self, id_mascota: int) -> Mascota:
        return self._mascota_dao.obtener_por_id_estricto(id_mascota)

    def listar_mascotas(self) -> list[Mascota]:
        return self._mascota_dao.listar_todos()

    def buscar_mascotas_por_nombre(self, termino: str) -> list[Mascota]:
        termino_limpio = termino.strip().casefold()
        if not termino_limpio:
            raise ValueError("Debe proporcionar un nombre para buscar.")
        return [
            mascota
            for mascota in self._mascota_dao.listar_todos()
            if termino_limpio in mascota.nombre.casefold()
        ]

    def buscar_mascotas_por_especie(self, termino: str) -> list[Mascota]:
        termino_limpio = termino.strip().casefold()
        if not termino_limpio:
            raise ValueError("Debe proporcionar una especie para buscar.")
        return [
            mascota
            for mascota in self._mascota_dao.listar_todos()
            if termino_limpio in mascota.especie.nombre_especie.casefold()
        ]

    def buscar_mascotas_por_edad(self, edad: int) -> list[Mascota]:
        if not isinstance(edad, int) or isinstance(edad, bool):
            raise TypeError("La edad debe ser un número entero.")
        if edad < 0:
            raise ValueError("La edad no puede ser negativa.")
        return [
            mascota
            for mascota in self._mascota_dao.listar_todos()
            if mascota.calcular_edad() == edad
        ]

    def registrar_mascota(self, mascota: Mascota) -> Mascota:
        if not isinstance(mascota, Mascota):
            raise TypeError("Debe proporcionar una mascota válida.")
        if mascota.id_propietario is None:
            raise ValueError("No se puede registrar una mascota sin dueño.")
        try:
            self._mascota_dao.insertar(mascota)
            return mascota
        except sqlite3.IntegrityError as error:
            nombre_limpio = mascota.nombre.strip()
            raise ValueError(f"No se pudo registrar: la mascota '{nombre_limpio}' ya existe en el sistema.") from error

    def actualizar_mascota(self, mascota: Mascota) -> bool:
        return self._mascota_dao.actualizar(mascota)

    def borrar_mascota(self, id_mascota: int) -> bool:
        return self._mascota_dao.eliminar(id_mascota)
