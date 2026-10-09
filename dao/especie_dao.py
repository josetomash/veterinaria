from database import ConexionDB
from models.especie import Especie


class EspecieDAO:
    def __init__(self, conexion_db: ConexionDB):
        self._db = conexion_db
        self.crear_tabla()

    def crear_tabla(self):
        ddl = """
            CREATE TABLE IF NOT EXISTS especies (
                id_especie INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL UNIQUE,
                informacion TEXT NOT NULL
            )
        """
        with self._db.obtener_conexion() as conn:
            conn.execute(ddl)

    def insertar(self, especie: Especie) -> None:
        sql = """
            INSERT INTO especies (id_especie, nombre, informacion)
            VALUES (?, ?, ?)
        """
        parametros = (especie.id_especie, especie.nombre_especie, especie.informacion_especie)
        with self._db.obtener_conexion() as conn:
            conn.execute(sql, parametros)

    def obtener_por_id_estricto(self, id_especie: int) -> Especie:
        sql = "SELECT id_especie FROM especies WHERE id_especie = ?"
        with self._db.obtener_conexion() as conn:
            fila = conn.execute(sql, (id_especie,)).fetchone()
        if fila is None:
            raise ValueError(f"No existe la especie con ID {id_especie}.")
        return next(especie for especie in Especie if especie.id_especie == fila[0])

    def listar_todos(self) -> list[Especie]:
        sql = "SELECT id_especie FROM especies ORDER BY nombre"
        with self._db.obtener_conexion() as conn:
            filas = conn.execute(sql).fetchall()
        return [next(especie for especie in Especie if especie.id_especie == fila[0]) for fila in filas]

    def actualizar(self, especie: Especie) -> bool:
        sql = "UPDATE especies SET nombre = ?, informacion = ? WHERE id_especie = ?"
        parametros = (especie.nombre_especie, especie.informacion_especie, especie.id_especie)
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, parametros)
            if cursor.rowcount == 0:
                raise ValueError(f"No existe la especie con ID {especie.id_especie}.")
        return True

    def eliminar(self, id_especie: int) -> bool:
        sql = "DELETE FROM especies WHERE id_especie = ?"
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, (id_especie,))
            if cursor.rowcount == 0:
                raise ValueError(f"No existe la especie con ID {id_especie}.")
        return True