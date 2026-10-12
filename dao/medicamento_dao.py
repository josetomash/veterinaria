import sqlite3
from models.medicamento import Medicamento

class MedicamentoDAO:
    def __init__(self, ruta_db: str = "database/clinica_veterinaria.db"):
        self.ruta_db = ruta_db
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.ruta_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS medicamentos (
                    id_medicamento INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_comercial TEXT NOT NULL UNIQUE,
                    cantidad_mg INTEGER NOT NULL CHECK(cantidad_mg > 0)
                )
            ''')
            conn.commit()

    def insertar(self, medicamento: Medicamento) -> None:
        query = """
            INSERT INTO medicamentos (nombre_comercial, cantidad_mg)
            VALUES (?, ?)
        """
        nombre_limpio = medicamento.nombre_comercial.strip()
        cantidad_mg = medicamento.cantidad_mg

        with sqlite3.connect(self.ruta_db) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (nombre_limpio, cantidad_mg))
            conn.commit()