from database.conexion import Conexion
from models.especie import Especie


class EspecieDAO:
    def __init__(self, ruta_db: str | Conexion = "database/clinica_veterinaria.db"):
        self.conexion = ruta_db if isinstance(ruta_db, Conexion) else Conexion(ruta_db)
        self._create_table()

    def _create_table(self):
        self.conexion.ejecutar(
            """
            CREATE TABLE IF NOT EXISTS especies (
                id_especie INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            )
            """
        )

    def insertar(self, especie: Especie) -> None:
        query = """
            INSERT INTO especies (nombre)
            VALUES (?)
        """
        nombre_limpio = especie.nombre_especie.strip()
        self.conexion.ejecutar(query, (nombre_limpio,))