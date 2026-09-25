import sqlite3
from models.especie import Especie

class EspecieDAO:
    def __init__(self, ruta_db: str = "database/clinica_veterinaria.db"):
        self.ruta_db = ruta_db
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.ruta_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS especies (
                    id_especie INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL UNIQUE
                )
            ''')
            conn.commit()

    def insertar(self, especie: Especie) -> None:
        query = """
            INSERT INTO especies (nombre)
            VALUES (?)
        """
        nombre_limpio = especie.value.strip()

        with sqlite3.connect(self.ruta_db) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (nombre_limpio,))
            conn.commit()