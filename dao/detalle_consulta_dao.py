from database import ConexionDB
from models.detalle_consulta import DetalleConsulta
from models.receta_medica import RecetaMedica


class DetalleConsultaDAO:
    def __init__(self, conexion_db: ConexionDB):
        self._db = conexion_db
        self.crear_tabla()

    def crear_tabla(self):
        ddl = """
            CREATE TABLE IF NOT EXISTS detalle_consulta (
                id_detalle INTEGER PRIMARY KEY,
                diagnostico TEXT NOT NULL,
                tratamiento TEXT NOT NULL,
                id_receta INTEGER NOT NULL,
                FOREIGN KEY (id_receta) REFERENCES receta_medica(id_receta)
            )
        """
        with self._db.obtener_conexion() as conn:
            conn.execute(ddl)

    def insertar(self, detalle: DetalleConsulta) -> None:
        sql = """
            INSERT INTO detalle_consulta (id_detalle, diagnostico, tratamiento, id_receta)
            VALUES (?, ?, ?, ?)
        """
        parametros = (detalle.id_detalle, detalle.diagnostico, detalle.tratamiento, detalle.receta.id_receta)
        with self._db.obtener_conexion() as conn:
            conn.execute(sql, parametros)

    def _crear_detalle(self, fila) -> DetalleConsulta:
        receta = RecetaMedica(fila[3], fila[4], fila[5], fila[6])
        return DetalleConsulta(fila[0], fila[1], fila[2], receta)

    def obtener_por_id_estricto(self, id_detalle: int) -> DetalleConsulta:
        sql = """
            SELECT d.id_detalle, d.diagnostico, d.tratamiento,
                   r.id_receta, r.nombre_comercial, r.cantidad_mg, r.instrucciones
            FROM detalle_consulta AS d
            JOIN receta_medica AS r ON r.id_receta = d.id_receta
            WHERE d.id_detalle = ?
        """
        with self._db.obtener_conexion() as conn:
            fila = conn.execute(sql, (id_detalle,)).fetchone()
        if fila is None:
            raise ValueError(f"No existe el detalle de consulta con ID {id_detalle}.")
        return self._crear_detalle(fila)

    def listar_todos(self) -> list[DetalleConsulta]:
        sql = """
            SELECT d.id_detalle, d.diagnostico, d.tratamiento,
                   r.id_receta, r.nombre_comercial, r.cantidad_mg, r.instrucciones
            FROM detalle_consulta AS d
            JOIN receta_medica AS r ON r.id_receta = d.id_receta
            ORDER BY d.id_detalle
        """
        with self._db.obtener_conexion() as conn:
            filas = conn.execute(sql).fetchall()
        return [self._crear_detalle(fila) for fila in filas]

    def actualizar(self, detalle: DetalleConsulta) -> bool:
        sql = """
            UPDATE detalle_consulta
            SET diagnostico = ?, tratamiento = ?, id_receta = ?
            WHERE id_detalle = ?
        """
        parametros = (
            detalle.diagnostico,
            detalle.tratamiento,
            detalle.receta.id_receta,
            detalle.id_detalle,
        )
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, parametros)
            if cursor.rowcount == 0:
                raise ValueError(f"No existe el detalle de consulta con ID {detalle.id_detalle}.")
        return True

    def eliminar(self, id_detalle: int) -> bool:
        sql = "DELETE FROM detalle_consulta WHERE id_detalle = ?"
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, (id_detalle,))
            if cursor.rowcount == 0:
                raise ValueError(f"No existe el detalle de consulta con ID {id_detalle}.")
        return True