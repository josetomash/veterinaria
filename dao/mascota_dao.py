from database.conexion import Conexion
from models.mascota import Mascota


class MascotaDAO:
    def __init__(self, ruta_db: str | Conexion = "database/clinica_veterinaria.db"):
        self.conexion = ruta_db if isinstance(ruta_db, Conexion) else Conexion(ruta_db)
        self._create_table()

    def _create_table(self):
        self.conexion.ejecutar(
            """
            CREATE TABLE IF NOT EXISTS mascotas (
                id_mascota INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                id_especie INTEGER NOT NULL,
                FOREIGN KEY (id_especie) REFERENCES especies(id_especie)
            )
            """
        )

    def insertar(self, mascota: Mascota) -> None:
        query = """
            INSERT INTO mascotas (nombre, id_especie)
            VALUES (?, ?)
        """
        nombre_limpio = mascota.nombre.strip()
        id_especie = mascota.especie.id_especie
        self.conexion.ejecutar(query, (nombre_limpio, id_especie))