from datetime import date

from database import ConexionDB
from models.consulta import Consulta


class ConsultaDAO:
    def __init__(self, conexion_db: ConexionDB):
        self._db = conexion_db
        self.crear_tabla()

    def crear_tabla(self):
        ddl = """
            CREATE TABLE IF NOT EXISTS consulta (
                id_consulta INTEGER PRIMARY KEY AUTOINCREMENT,
                id_mascota INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                motivo TEXT NOT NULL,
                veterinario_id INTEGER NOT NULL,
                propietario_id INTEGER NOT NULL,
                FOREIGN KEY (id_mascota) REFERENCES mascotas(id_mascota),
                FOREIGN KEY (veterinario_id) REFERENCES veterinarios(id_veterinario),
                FOREIGN KEY (propietario_id) REFERENCES propietarios(id_propietario)
            )
        """
        with self._db.obtener_conexion() as conn:
            conn.execute(ddl)

    def insertar(self, consulta: Consulta) -> None:
        sql = """
            INSERT INTO consulta (
                id_consulta, id_mascota, fecha, motivo, veterinario_id, propietario_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """
        parametros = (
            consulta.id_consulta,
            consulta.mascota_id,
            consulta.fecha_consulta.isoformat(),
            consulta.motivo,
            consulta.veterinario_id,
            consulta.propietario_id,
        )
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, parametros)
            # La base de datos asigna el ID automáticamente
            consulta.id_consulta = cursor.lastrowid

    def obtener_por_id_estricto(self, id_consulta: int) -> Consulta:
        sql = """
            SELECT id_consulta, motivo, fecha, veterinario_id, id_mascota, propietario_id
            FROM consulta
            WHERE id_consulta = ?
        """
        with self._db.obtener_conexion() as conn:
            fila = conn.execute(sql, (id_consulta,)).fetchone()
        if fila is None:
            raise ValueError(f"No existe la consulta con ID {id_consulta}.")
        # Tupla: (id_consulta, motivo, fecha, veterinario_id, id_mascota, propietario_id)
        return Consulta(
            fila[0],
            fila[1],
            date.fromisoformat(fila[2]),
            fila[3],
            fila[4],
            fila[5],
        )

    def listar_todos(self) -> list[Consulta]:
        sql = """
            SELECT id_consulta, motivo, fecha, veterinario_id, id_mascota, propietario_id
            FROM consulta
            ORDER BY id_consulta
        """
        consultas = []
        with self._db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()

            for fila in filas:
                # Tupla: (id_consulta, motivo, fecha, veterinario_id, id_mascota, propietario_id)
                consulta = Consulta(
                    fila[0],
                    fila[1],
                    date.fromisoformat(fila[2]),
                    fila[3],
                    fila[4],
                    fila[5],
                )
                consultas.append(consulta)
        return consultas

    def actualizar(self, consulta: Consulta) -> bool:
        sql = """
            UPDATE consulta
            SET id_mascota = ?, fecha = ?, motivo = ?, veterinario_id = ?, propietario_id = ?
            WHERE id_consulta = ?
        """
        parametros = (
            consulta.mascota_id,
            consulta.fecha_consulta.isoformat(),
            consulta.motivo,
            consulta.veterinario_id,
            consulta.propietario_id,
            consulta.id_consulta,
        )
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, parametros)
            if cursor.rowcount == 0:
                raise ValueError(f"No existe la consulta con ID {consulta.id_consulta}.")
        return True

    def eliminar(self, id_consulta: int) -> bool:
        sql = "DELETE FROM consulta WHERE id_consulta = ?"
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, (id_consulta,))
            if cursor.rowcount == 0:
                raise ValueError(f"No existe la consulta con ID {id_consulta}.")
        return True