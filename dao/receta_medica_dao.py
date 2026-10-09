from database import ConexionDB
from models.receta_medica import RecetaMedica


class RecetaMedicaDAO:
    def __init__(self, conexion_db: ConexionDB):
        self._db = conexion_db
        self.crear_tabla()

    def crear_tabla(self):
        ddl = """
            CREATE TABLE IF NOT EXISTS receta_medica (
                id_receta INTEGER PRIMARY KEY,
                nombre_comercial TEXT NOT NULL,
                cantidad_mg INTEGER NOT NULL CHECK(cantidad_mg >= 0),
                instrucciones TEXT NOT NULL
            )
        """
        with self._db.obtener_conexion() as conn:
            conn.execute(ddl)

    def insertar(self, receta: RecetaMedica) -> None:
        sql = """
            INSERT INTO receta_medica (id_receta, nombre_comercial, cantidad_mg, instrucciones)
            VALUES (?, ?, ?, ?)
        """
        parametros = (receta.id_receta, receta.nombre_comercial, receta.cantidad_mg, receta.instrucciones)
        with self._db.obtener_conexion() as conn:
            conn.execute(sql, parametros)

    def obtener_por_id_estricto(self, id_receta: int) -> RecetaMedica:
        sql = """
            SELECT id_receta, nombre_comercial, cantidad_mg, instrucciones
            FROM receta_medica
            WHERE id_receta = ?
        """
        with self._db.obtener_conexion() as conn:
            fila = conn.execute(sql, (id_receta,)).fetchone()
        if fila is None:
            raise ValueError(f"No existe la receta médica con ID {id_receta}.")
        return RecetaMedica(*fila)

    def listar_todos(self) -> list[RecetaMedica]:
        sql = """
            SELECT id_receta, nombre_comercial, cantidad_mg, instrucciones
            FROM receta_medica
            ORDER BY nombre_comercial
        """
        with self._db.obtener_conexion() as conn:
            filas = conn.execute(sql).fetchall()
        return [RecetaMedica(*fila) for fila in filas]

    def actualizar(self, receta: RecetaMedica) -> bool:
        sql = """
            UPDATE receta_medica
            SET nombre_comercial = ?, cantidad_mg = ?, instrucciones = ?
            WHERE id_receta = ?
        """
        parametros = (
            receta.nombre_comercial,
            receta.cantidad_mg,
            receta.instrucciones,
            receta.id_receta,
        )
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, parametros)
            if cursor.rowcount == 0:
                raise ValueError(f"No existe la receta médica con ID {receta.id_receta}.")
        return True

    def eliminar(self, id_receta: int) -> bool:
        sql = "DELETE FROM receta_medica WHERE id_receta = ?"
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, (id_receta,))
            if cursor.rowcount == 0:
                raise ValueError(f"No existe la receta médica con ID {id_receta}.")
        return True