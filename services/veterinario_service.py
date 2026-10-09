import sqlite3

from dao import VeterinarioDAO
from models import Veterinario


class VeterinarioService:
    def __init__(self, veterinario_dao: VeterinarioDAO):
        self._veterinario_dao = veterinario_dao

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
