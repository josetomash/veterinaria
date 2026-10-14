from datetime import date

from database import ConexionDB
from models.consulta import Consulta
from models.detalle_consulta import DetalleConsulta
from models.especialidad import Especialidad
from models.receta_medica import RecetaMedica
from models.veterinario import Veterinario


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
                id_consulta INTEGER,
                FOREIGN KEY (id_consulta) REFERENCES consulta(id_consulta),
                FOREIGN KEY (id_receta) REFERENCES receta_medica(id_receta)
            )
        """
        with self._db.obtener_conexion() as conn:
            conn.execute(ddl)
            columnas = {
                fila[1] for fila in conn.execute("PRAGMA table_info(detalle_consulta)")
            }
            if "id_consulta" not in columnas:
                conn.execute(
                    "ALTER TABLE detalle_consulta "
                    "ADD COLUMN id_consulta INTEGER REFERENCES consulta(id_consulta)"
                )

    def insertar(self, detalle: DetalleConsulta) -> None:
        consulta = detalle.consulta
        if consulta is None:
            raise ValueError("El detalle debe estar asociado a una consulta.")
        sql = """
            INSERT INTO detalle_consulta (
                id_detalle, diagnostico, tratamiento, id_receta, id_consulta
            )
            VALUES (?, ?, ?, ?, ?)
        """
        parametros = (
            detalle.id_detalle,
            detalle.diagnostico,
            detalle.tratamiento,
            detalle.receta.id_receta,
            consulta.id_consulta,
        )
        with self._db.obtener_conexion() as conn:
            conn.execute(sql, parametros)

    def obtener_por_id_estricto(self, id_detalle: int) -> DetalleConsulta:
        sql_detalle = """
            SELECT id_detalle, diagnostico, tratamiento, id_receta, id_consulta
            FROM detalle_consulta
            WHERE id_detalle = ?
        """
        sql_receta = """
            SELECT r.id_receta, r.nombre_comercial, r.cantidad_mg, r.instrucciones,
                   v.id_veterinario, v.nombre, v.rut, v.telefono, v.especialidad
            FROM receta_medica AS r
            LEFT JOIN veterinarios AS v ON v.id_veterinario = r.id_veterinario
            WHERE r.id_receta = ?
        """
        with self._db.obtener_conexion() as conn:
            fila_detalle = conn.execute(sql_detalle, (id_detalle,)).fetchone()
            if fila_detalle is None:
                raise ValueError(f"No existe el detalle de consulta con ID {id_detalle}.")
            # Tupla: (id_detalle, diagnostico, tratamiento, id_receta, id_consulta)
            fila_receta = conn.execute(sql_receta, (fila_detalle[3],)).fetchone()
            fila_consulta = None
            if fila_detalle[4] is not None:
                fila_consulta = conn.execute(
                    """
                    SELECT id_consulta, motivo, fecha, veterinario_id,
                           id_mascota, propietario_id
                    FROM consulta
                    WHERE id_consulta = ?
                    """,
                    (fila_detalle[4],),
                ).fetchone()
        if fila_receta is None:
            raise ValueError(
                f"No se encontró la receta asociada al detalle de consulta con ID {id_detalle}."
            )
        if fila_detalle[4] is not None and fila_consulta is None:
            raise ValueError(
                f"No se encontró la consulta asociada al detalle con ID {id_detalle}."
            )
        veterinario = None
        if fila_receta[4] is not None:
            veterinario = Veterinario(
                fila_receta[4],
                fila_receta[5],
                fila_receta[6],
                fila_receta[7],
                Especialidad(fila_receta[8]),
            )
        receta = RecetaMedica(*fila_receta[:4], veterinario)
        consulta = None
        if fila_consulta is not None:
            consulta = Consulta(
                fila_consulta[0],
                fila_consulta[1],
                date.fromisoformat(fila_consulta[2]),
                fila_consulta[3],
                fila_consulta[4],
                fila_consulta[5],
            )
        return DetalleConsulta(
            fila_detalle[0],
            fila_detalle[1],
            fila_detalle[2],
            receta,
            consulta,
        )

    def listar_todos(self) -> list[DetalleConsulta]:
        sql_detalles = """
            SELECT id_detalle, diagnostico, tratamiento, id_receta, id_consulta
            FROM detalle_consulta
            ORDER BY id_detalle
        """
        sql_receta = """
            SELECT r.id_receta, r.nombre_comercial, r.cantidad_mg, r.instrucciones,
                   v.id_veterinario, v.nombre, v.rut, v.telefono, v.especialidad
            FROM receta_medica AS r
            LEFT JOIN veterinarios AS v ON v.id_veterinario = r.id_veterinario
            WHERE r.id_receta = ?
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
                        # Tupla fila_detalle: (id_detalle, diagnostico, tratamiento, id_receta)
                        f"con ID {fila_detalle[0]}."
                    )
                consulta = None
                if fila_detalle[4] is not None:
                    fila_consulta = cursor.execute(
                        """
                        SELECT id_consulta, motivo, fecha, veterinario_id,
                               id_mascota, propietario_id
                        FROM consulta
                        WHERE id_consulta = ?
                        """,
                        (fila_detalle[4],),
                    ).fetchone()
                    if fila_consulta is None:
                        raise ValueError(
                            f"No se encontró la consulta asociada al detalle con ID {fila_detalle[0]}."
                        )
                    consulta = Consulta(
                        fila_consulta[0],
                        fila_consulta[1],
                        date.fromisoformat(fila_consulta[2]),
                        fila_consulta[3],
                        fila_consulta[4],
                        fila_consulta[5],
                    )
                veterinario = None
                if fila_receta[4] is not None:
                    veterinario = Veterinario(
                        fila_receta[4],
                        fila_receta[5],
                        fila_receta[6],
                        fila_receta[7],
                        Especialidad(fila_receta[8]),
                    )
                receta = RecetaMedica(*fila_receta[:4], veterinario)
                detalle = DetalleConsulta(
                    fila_detalle[0],
                    fila_detalle[1],
                    fila_detalle[2],
                    receta,
                    consulta,
                )
                detalles.append(detalle)
        return detalles

    def actualizar(self, detalle: DetalleConsulta) -> bool:
        consulta = detalle.consulta
        if consulta is None:
            raise ValueError("El detalle debe estar asociado a una consulta.")
        sql = """
            UPDATE detalle_consulta
            SET diagnostico = ?, tratamiento = ?, id_receta = ?, id_consulta = ?
            WHERE id_detalle = ?
        """
        parametros = (
            detalle.diagnostico,
            detalle.tratamiento,
            detalle.receta.id_receta,
            consulta.id_consulta,
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