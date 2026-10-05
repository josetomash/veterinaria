import sqlite3
from models.veterinario import Veterinario

class VeterinarioDAO:
    def __init__(self, ruta_db: str = "database/clinica_veterinaria.db"):
        self.ruta_db = ruta_db
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.ruta_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS veterinarios (
                    id_veterinario INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    especialidad TEXT NOT NULL
                )
            ''')
            conn.commit()

    def insertar(self, veterinario: Veterinario) -> None:
        query = """
            INSERT INTO veterinarios (nombre, especialidad)
            VALUES (?, ?)
        """
        nombre_limpio = veterinario.nombre.strip()
        especialidad_str = veterinario.especialidad.value.strip() if hasattr(veterinario.especialidad, 'value') else str(veterinario.especialidad).strip()

        with sqlite3.connect(self.ruta_db) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (nombre_limpio, especialidad_str))
            conn.commit()