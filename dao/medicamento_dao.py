from database.conexion import Conexion
from models.medicamento import Medicamento


class MedicamentoDAO:
    def __init__(self, ruta_db: str | Conexion = "database/clinica_veterinaria.db"):
        self.conexion = ruta_db if isinstance(ruta_db, Conexion) else Conexion(ruta_db)
        self._create_table()

    def _create_table(self):
        self.conexion.ejecutar(
            """
            CREATE TABLE IF NOT EXISTS medicamentos (
                id_medicamento INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_comercial TEXT NOT NULL UNIQUE,
                cantidad_mg INTEGER NOT NULL CHECK(cantidad_mg > 0)
            )
            """
        )

    def insertar(self, medicamento: Medicamento) -> None:
        query = """
            INSERT INTO medicamentos (nombre_comercial, cantidad_mg)
            VALUES (?, ?)
        """
        nombre_limpio = medicamento.nombre_comercial.strip()
        cantidad_mg = medicamento.cantidad_mg

        self.conexion.ejecutar(query, (nombre_limpio, cantidad_mg))