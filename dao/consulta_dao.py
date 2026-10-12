import sqlite3
from models.consulta import Consulta

class ConsultaDAO:
    def __init__(self, ruta_db: str = "database/clinica_veterinaria.db"):
        self.ruta_db = ruta_db
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.ruta_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS consulta (
                    id_consulta INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_mascota INTEGER NOT NULL,
                    fecha TEXT NOT NULL,
                    motivo TEXT NOT NULL,
                    FOREIGN KEY (id_mascota) REFERENCES mascota(id_mascota)
                )
            ''')
            conn.commit()

    def insertar(self, consulta: Consulta) -> None:
        query = """
            INSERT INTO consulta (id_mascota, fecha, motivo)
            VALUES (?, ?, ?)
        """
        with sqlite3.connect(self.ruta_db) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (consulta.id_mascota, consulta.fecha, consulta.motivo))
            conn.commit()