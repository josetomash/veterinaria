from pathlib import Path
import sqlite3
from typing import Sequence


class Conexion:
    def __init__(self, ruta_db: str = "database/clinica_veterinaria.db"):
        self.ruta_db = ruta_db
        if ruta_db != ":memory:":
            Path(ruta_db).parent.mkdir(parents=True, exist_ok=True)
        self._conexion = sqlite3.connect(ruta_db)

    def ejecutar(
        self,
        query: str,
        parametros: Sequence[object] = (),
    ) -> sqlite3.Cursor:
        try:
            cursor = self._conexion.execute(query, parametros)
            self._conexion.commit()
            return cursor
        except sqlite3.Error:
            self._conexion.rollback()
            raise

    def consultar(
        self,
        query: str,
        parametros: Sequence[object] = (),
    ) -> list[tuple[object, ...]]:
        return self._conexion.execute(query, parametros).fetchall()

    def cerrar(self) -> None:
        self._conexion.close()

