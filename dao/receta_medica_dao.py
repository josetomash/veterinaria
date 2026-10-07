from database.conexion import Conexion
from models.receta_medica import RecetaMedica


class RecetaMedicaDAO:
    def __init__(self, ruta_db: str | Conexion = "database/clinica_veterinaria.db"):
        self.conexion = ruta_db if isinstance(ruta_db, Conexion) else Conexion(ruta_db)
        self._create_table()

    def _create_table(self):
        self.conexion.ejecutar(
            """
            CREATE TABLE IF NOT EXISTS receta_medica (
                id_receta INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_comercial TEXT NOT NULL,
                cantidad_mg INTEGER NOT NULL CHECK(cantidad_mg >= 0),
                instrucciones TEXT NOT NULL
            )
            """
        )

    def insertar(self, receta: RecetaMedica) -> None:
        query = """
            INSERT INTO receta_medica (nombre_comercial, cantidad_mg, instrucciones)
            VALUES (?, ?, ?)
        """
        nombre_limpio = receta.nombre_comercial.strip()
        cantidad_mg = receta.cantidad_mg
        instrucciones_limpias = receta.instrucciones.strip()

        self.conexion.ejecutar(query, (nombre_limpio, cantidad_mg, instrucciones_limpias))