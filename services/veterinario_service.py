import sqlite3

from dao import VeterinarioDAO
from models import Veterinario


class VeterinarioService:
    def __init__(self, veterinario_dao: VeterinarioDAO):
        self._veterinario_dao = veterinario_dao

    def obtener_veterinario_por_id(self, id_veterinario: int) -> Veterinario:
        return self._veterinario_dao.obtener_por_id_estricto(id_veterinario)

    def listar_veterinarios(self) -> list[Veterinario]:
        return self._veterinario_dao.listar_todos()

    def registrar_veterinario(self, veterinario: Veterinario) -> Veterinario:
        if not isinstance(veterinario, Veterinario):
            raise TypeError("Debe proporcionar un veterinario válido.")
        try:
            self._veterinario_dao.insertar(veterinario)
            return veterinario
        except sqlite3.IntegrityError as error:
            nombre_limpio = veterinario.nombre.strip()
            raise ValueError(
                f"No se pudo registrar: el veterinario '{nombre_limpio}' ya existe en el sistema."
            ) from error

    def actualizar_veterinario(self, veterinario: Veterinario) -> bool:
        return self._veterinario_dao.actualizar(veterinario)

    def borrar_veterinario(self, id_veterinario: int) -> bool:
        return self._veterinario_dao.eliminar(id_veterinario)
