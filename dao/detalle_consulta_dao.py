import sqlite3
from models.detalle_consulta import DetalleConsulta

class DetalleConsultaDAO:
    def __init__(self, ruta_db: str = "database/clinica_veterinaria.db"):
        self.ruta_db = ruta_db
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.ruta_db) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS detalle_consulta (
                    id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_consulta INTEGER NOT NULL,
                    id_medicamento INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
                    FOREIGN KEY (id_consulta) REFERENCES consulta(id_consulta),
                    FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id_medicamento)
                )
            ''')
            conn.commit()

    def insertar(self, detalle: DetalleConsulta) -> None:
        query = """
            INSERT INTO detalle_consulta (id_consulta, id_medicamento, cantidad)
            VALUES (?, ?, ?)
        """
        with sqlite3.connect(self.ruta_db) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (detalle.id_consulta, detalle.id_medicamento, detalle.cantidad))
            conn.commit()