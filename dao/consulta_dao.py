from database.conexion import Conexion
from models.consulta import Consulta


class ConsultaDAO:
    def __init__(self, ruta_db: str | Conexion = "database/clinica_veterinaria.db"):
        self.conexion = ruta_db if isinstance(ruta_db, Conexion) else Conexion(ruta_db)
        self._create_table()

    def _create_table(self):
        self.conexion.ejecutar(
            """
            CREATE TABLE IF NOT EXISTS consulta (
                id_consulta INTEGER PRIMARY KEY AUTOINCREMENT,
                id_mascota INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                motivo TEXT NOT NULL,
                FOREIGN KEY (id_mascota) REFERENCES mascota(id_mascota)
            )
            """
        )

    def insertar(self, consulta: Consulta) -> None:
        query = """
            INSERT INTO consulta (id_mascota, fecha, motivo)
            VALUES (?, ?, ?)
        """
        parametros = (consulta.mascota_id, consulta.fecha_consulta.isoformat(), consulta.motivo)
        self.conexion.ejecutar(query, parametros)