from database import ConexionDB
from models.especialidad import Especialidad
from models.veterinario import Veterinario


class VeterinarioDAO:
    def __init__(self, conexion_db: ConexionDB):
        self._db = conexion_db
        self.crear_tabla()

    def crear_tabla(self):
        ddl = """
            CREATE TABLE IF NOT EXISTS veterinarios (
                id_veterinario INTEGER PRIMARY KEY,
                id_persona INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                rut TEXT NOT NULL UNIQUE,
                telefono TEXT NOT NULL,
                especialidad TEXT NOT NULL,
                FOREIGN KEY (especialidad) REFERENCES especialidades(nombre)
            )
        """
        with self._db.obtener_conexion() as conn:
            conn.execute(ddl)

    def insertar(self, veterinario: Veterinario) -> None:
        sql = """
            INSERT INTO veterinarios (
                id_veterinario, id_persona, nombre, rut, telefono, especialidad
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """
        parametros = (
            veterinario.id_veterinario,
            veterinario.id_persona,
            veterinario.nombre,
            veterinario.rut,
            veterinario.telefono,
            veterinario.especialidad.value,
        )
        with self._db.obtener_conexion() as conn:
            conn.execute("INSERT OR IGNORE INTO especialidades (nombre) VALUES (?)", (veterinario.especialidad.value,))
            conn.execute(sql, parametros)

    def obtener_por_id_estricto(self, id_veterinario: int) -> Veterinario:
        sql = """
            SELECT id_persona, nombre, rut, telefono, id_veterinario, especialidad
            FROM veterinarios
            WHERE id_veterinario = ?
        """
        with self._db.obtener_conexion() as conn:
            fila = conn.execute(sql, (id_veterinario,)).fetchone()
        if fila is None:
            raise ValueError(f"No existe el veterinario con ID {id_veterinario}.")
        return Veterinario(*fila[:5], Especialidad(fila[5]))

    def listar_todos(self) -> list[Veterinario]:
        sql = """
            SELECT id_persona, nombre, rut, telefono, id_veterinario, especialidad
            FROM veterinarios
            ORDER BY nombre
        """
        with self._db.obtener_conexion() as conn:
            filas = conn.execute(sql).fetchall()
        return [Veterinario(*fila[:5], Especialidad(fila[5])) for fila in filas]

    def actualizar(self, veterinario: Veterinario) -> bool:
        sql = """
            UPDATE veterinarios
            SET id_persona = ?, nombre = ?, rut = ?, telefono = ?, especialidad = ?
            WHERE id_veterinario = ?
        """
        parametros = (
            veterinario.id_persona,
            veterinario.nombre,
            veterinario.rut,
            veterinario.telefono,
            veterinario.especialidad.value,
            veterinario.id_veterinario,
        )
        with self._db.obtener_conexion() as conn:
            conn.execute("INSERT OR IGNORE INTO especialidades (nombre) VALUES (?)", (veterinario.especialidad.value,))
            cursor = conn.execute(sql, parametros)
            if cursor.rowcount == 0:
                raise ValueError(f"No existe el veterinario con ID {veterinario.id_veterinario}.")
        return True

    def eliminar(self, id_veterinario: int) -> bool:
        sql = "DELETE FROM veterinarios WHERE id_veterinario = ?"
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, (id_veterinario,))
            if cursor.rowcount == 0:
                raise ValueError(f"No existe el veterinario con ID {id_veterinario}.")
        return True