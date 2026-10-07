from database.conexion import Conexion
from models.detalle_consulta import DetalleConsulta


class DetalleConsultaDAO:
    def __init__(self, ruta_db: str | Conexion = "database/clinica_veterinaria.db"):
        self.conexion = ruta_db if isinstance(ruta_db, Conexion) else Conexion(ruta_db)
        self._create_table()

    def _create_table(self):
        self.conexion.ejecutar(
            """
            CREATE TABLE IF NOT EXISTS detalle_consulta (
                id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                id_consulta INTEGER NOT NULL,
                id_medicamento INTEGER NOT NULL,
                cantidad INTEGER NOT NULL CHECK(cantidad > 0),
                FOREIGN KEY (id_consulta) REFERENCES consulta(id_consulta),
                FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id_medicamento)
            )
            """
        )

    def insertar(self, detalle: DetalleConsulta) -> None:
        query = """
            INSERT INTO detalle_consulta (id_consulta, id_medicamento, cantidad)
            VALUES (?, ?, ?)
        """
        self.conexion.ejecutar(query, (detalle.id_consulta, detalle.id_medicamento, detalle.cantidad))