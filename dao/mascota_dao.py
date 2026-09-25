import sqlite3
from models.mascota import Mascota

class MascotaDAO:
    def __init__(self, ruta_db: str = "database/clinica_veterinaria.db"):
        self.ruta_db = ruta_db
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.ruta_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mascotas (
                    id_mascota INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    id_especie INTEGER NOT NULL,
                    FOREIGN KEY (id_especie) REFERENCES especies(id_especie)
                )
            ''')
            conn.commit()

    def insertar(self, mascota: Mascota) -> None:
        query = """
            INSERT INTO mascotas (nombre, id_especie)
            VALUES (?, ?)
        """
        nombre_limpio = mascota.nombre.strip()
        id_especie = mascota.id_especie

        with sqlite3.connect(self.ruta_db) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (nombre_limpio, id_especie))
            conn.commit()