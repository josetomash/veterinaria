from database import ConexionDB
from models.especialidad import Especialidad


class EspecialidadDAO:
    def __init__(self, conexion_db: ConexionDB):
        self._db = conexion_db
        self.crear_tabla()

    def crear_tabla(self):
        ddl = """
            CREATE TABLE IF NOT EXISTS especialidades (
                nombre TEXT PRIMARY KEY
            )
        """
        with self._db.obtener_conexion() as conn:
            conn.execute(ddl)

    def insertar(self, especialidad: Especialidad) -> None:
        sql = "INSERT INTO especialidades (nombre) VALUES (?)"
        with self._db.obtener_conexion() as conn:
            conn.execute(sql, (especialidad.value,))

    def obtener_por_nombre_estricto(self, nombre: str) -> Especialidad:
        sql = "SELECT nombre FROM especialidades WHERE nombre = ?"
        with self._db.obtener_conexion() as conn:
            fila = conn.execute(sql, (nombre,)).fetchone()
        if fila is None:
            raise ValueError(f"No existe la especialidad '{nombre}'.")
        # Tupla: (nombre,)
        return Especialidad(fila[0])

    def listar_todos(self) -> list[Especialidad]:
        sql = "SELECT nombre FROM especialidades ORDER BY nombre"
        especialidades = []
        with self._db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()

            for fila in filas:
                # Tupla: (nombre,)
                especialidad = Especialidad(fila[0])
                especialidades.append(especialidad)
        return especialidades

