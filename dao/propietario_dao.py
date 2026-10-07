from database.conexion import Conexion
from models.propietario import Propietario


class PropietarioDAO:
    def __init__(self, ruta_db: str | Conexion = "database/clinica_veterinaria.db"):
        self.conexion = ruta_db if isinstance(ruta_db, Conexion) else Conexion(ruta_db)
        self._create_table()

    def _create_table(self):
        self.conexion.ejecutar(
            """
            CREATE TABLE IF NOT EXISTS propietarios (
                id_propietario INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                rut TEXT NOT NULL UNIQUE,
                telefono TEXT NOT NULL,
                email TEXT NOT NULL
            )
            """
        )
    
    def insertar(self, propietario: Propietario) -> None:
        query = """
            INSERT INTO propietarios (
                id_propietario,
                nombre,
                rut,
                telefono,
                email
            )
            VALUES (?, ?, ?, ?, ?)
        """
        parametros = (
            propietario.id_propietario,
            propietario.nombre.strip(),
            propietario.rut.strip(),
            propietario.telefono.strip(),
            propietario.email.strip(),
        )
        self.conexion.ejecutar(query, parametros)