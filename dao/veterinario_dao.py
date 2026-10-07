from database.conexion import Conexion
from models.veterinario import Veterinario


class VeterinarioDAO:
    def __init__(self, ruta_db: str | Conexion = "database/clinica_veterinaria.db"):
        self.conexion = ruta_db if isinstance(ruta_db, Conexion) else Conexion(ruta_db)
        self._create_table()

    def _create_table(self):
        self.conexion.ejecutar(
            """
            CREATE TABLE IF NOT EXISTS veterinarios (
                id_veterinario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                especialidad TEXT NOT NULL
            )
            """
        )

    def insertar(self, veterinario: Veterinario) -> None:
        query = """
            INSERT INTO veterinarios (nombre, especialidad)
            VALUES (?, ?)
        """
        nombre_limpio = veterinario.nombre.strip()
        especialidad_str = veterinario.especialidad.value.strip() if hasattr(veterinario.especialidad, 'value') else str(veterinario.especialidad).strip()

        self.conexion.ejecutar(query, (nombre_limpio, especialidad_str))