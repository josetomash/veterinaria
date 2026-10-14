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
                id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                diagnostico TEXT NOT NULL,
                tratamiento TEXT NOT NULL,
                id_receta INTEGER NOT NULL,
                id_consulta INTEGER,
                FOREIGN KEY (id_receta) REFERENCES receta_medica(id_receta),
                FOREIGN KEY (id_consulta) REFERENCES consulta(id_consulta)
            )
        """
        with self._db.obtener_conexion() as conn:
            conn.execute(ddl)
            # Bases antiguas: se agrega la columna que une el detalle con su consulta
            columnas = {
                fila[1] for fila in conn.execute("PRAGMA table_info(detalle_consulta)")
            }
            if "id_consulta" not in columnas:
                conn.execute(
                    "ALTER TABLE detalle_consulta "
                    "ADD COLUMN id_consulta INTEGER REFERENCES consulta(id_consulta)"
                )

    def insertar(self, detalle: DetalleConsulta) -> None:
        sql = """
            INSERT INTO detalle_consulta (id_detalle, diagnostico, tratamiento, id_receta, id_consulta)
            VALUES (?, ?, ?, ?, ?)
        """
        parametros = (
            detalle.id_detalle,
            detalle.diagnostico,
            detalle.tratamiento,
            detalle.receta.id_receta,
            detalle.id_consulta,
        )
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, parametros)
            # La base de datos asigna el ID automáticamente
            detalle.id_detalle = cursor.lastrowid

    def _crear_detalle(self, fila_detalle, fila_receta) -> DetalleConsulta:
        # Tuplas: fila_detalle=(id_detalle, diagnostico, tratamiento, id_receta, id_consulta);
        # fila_receta=(id_receta, nombre_comercial, cantidad_mg, instrucciones)
        receta = RecetaMedica(*fila_receta)
        return DetalleConsulta(
            fila_detalle[0],
            fila_detalle[1],
            fila_detalle[2],
            receta,
            fila_detalle[4],
        )

    def obtener_por_id_estricto(self, id_detalle: int) -> DetalleConsulta:
        sql_detalle = """
            SELECT id_detalle, diagnostico, tratamiento, id_receta, id_consulta
            FROM detalle_consulta
            WHERE id_detalle = ?
        """
        sql_receta = """
            SELECT id_receta, nombre_comercial, cantidad_mg, instrucciones
            FROM receta_medica
            WHERE id_receta = ?
        """
        with self._db.obtener_conexion() as conn:
            fila_detalle = conn.execute(sql_detalle, (id_detalle,)).fetchone()
            if fila_detalle is None:
                raise ValueError(f"No existe el detalle de consulta con ID {id_detalle}.")
            # Tupla: (id_detalle, diagnostico, tratamiento, id_receta, id_consulta)
            fila_receta = conn.execute(sql_receta, (fila_detalle[3],)).fetchone()
        if fila_receta is None:
            raise ValueError(
                f"No se encontró la receta asociada al detalle de consulta con ID {id_detalle}."
            )
        return self._crear_detalle(fila_detalle, fila_receta)

    def listar_todos(self) -> list[DetalleConsulta]:
        sql_detalles = """
            SELECT id_detalle, diagnostico, tratamiento, id_receta, id_consulta
            FROM detalle_consulta
            ORDER BY id_detalle
        """
        sql_receta = """
            SELECT id_receta, nombre_comercial, cantidad_mg, instrucciones
            FROM receta_medica
            WHERE id_receta = ?
        """
        detalles = []
        with self._db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_detalles)
            filas_detalle = cursor.fetchall()

            for fila_detalle in filas_detalle:
                # Tupla: (id_detalle, diagnostico, tratamiento, id_receta, id_consulta)
                cursor.execute(sql_receta, (fila_detalle[3],))
                fila_receta = cursor.fetchone()
                if fila_receta is None:
                    raise ValueError(
                        "No se encontró la receta asociada al detalle de consulta "
                        # Tupla fila_detalle: (id_detalle, diagnostico, tratamiento, id_receta, id_consulta)
                        f"con ID {fila_detalle[0]}."
                    )
                detalles.append(self._crear_detalle(fila_detalle, fila_receta))
        return detalles

    def actualizar(self, detalle: DetalleConsulta) -> bool:
        sql = """
            UPDATE detalle_consulta
            SET diagnostico = ?, tratamiento = ?, id_receta = ?, id_consulta = ?
            WHERE id_detalle = ?
        """
        parametros = (
            detalle.diagnostico,
            detalle.tratamiento,
            detalle.receta.id_receta,
            detalle.id_consulta,
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