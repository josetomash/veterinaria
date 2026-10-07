from database.conexion import Conexion
from models.especialidad import Especialidad


class EspecialidadDAO:
    def __init__(self, ruta_db: str | Conexion = "database/clinica_veterinaria.db"):
        self.conexion = ruta_db if isinstance(ruta_db, Conexion) else Conexion(ruta_db)
        self._create_table()

    def _create_table(self):
        self.conexion.ejecutar(
            """
            CREATE TABLE IF NOT EXISTS especialidades (
                id_especialidad INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            )
            """
        )

    def insertar(self, especialidad: Especialidad) -> None:
        query = """
            INSERT INTO especialidades (nombre)
            VALUES (?)
        """
        nombre_limpio = especialidad.value.strip()
        self.conexion.ejecutar(query, (nombre_limpio,))