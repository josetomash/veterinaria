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
                id_veterinario INTEGER PRIMARY KEY AUTOINCREMENT,
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
                id_veterinario, nombre, rut, telefono, especialidad
            )
            VALUES (?, ?, ?, ?, ?)
        """
        parametros = (
            veterinario.id_veterinario,
            veterinario.nombre,
            veterinario.rut,
            veterinario.telefono,
            veterinario.especialidad.value,
        )
        with self._db.obtener_conexion() as conn:
            conn.execute("INSERT OR IGNORE INTO especialidades (nombre) VALUES (?)", (veterinario.especialidad.value,))
            cursor = conn.execute(sql, parametros)
            # La base de datos asigna el ID automáticamente
            veterinario.id_veterinario = cursor.lastrowid

    def obtener_por_id_estricto(self, id_veterinario: int) -> Veterinario:
        sql = """
            SELECT id_veterinario, nombre, rut, telefono, especialidad
            FROM veterinarios
            WHERE id_veterinario = ?
        """
        with self._db.obtener_conexion() as conn:
            fila = conn.execute(sql, (id_veterinario,)).fetchone()
        if fila is None:
            raise ValueError(f"No existe el veterinario con ID {id_veterinario}.")
        # Tupla: (id_veterinario, nombre, rut, telefono, especialidad)
        return Veterinario(
            fila[0],
            fila[1],
            fila[2],
            fila[3],
            Especialidad(fila[4]),
        )

    def listar_todos(self) -> list[Veterinario]:
        sql = """
            SELECT id_veterinario, nombre, rut, telefono, especialidad
            FROM veterinarios
            ORDER BY id_veterinario
        """
        veterinarios = []
        with self._db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()

            for fila in filas:
                # Tupla: (id_veterinario, nombre, rut, telefono, especialidad)
                veterinario = Veterinario(
                    fila[0],
                    fila[1],
                    fila[2],
                    fila[3],
                    Especialidad(fila[4]),
                )
                veterinarios.append(veterinario)
        return veterinarios

    def actualizar(self, veterinario: Veterinario) -> bool:
        sql = """
            UPDATE veterinarios
            SET nombre = ?, rut = ?, telefono = ?, especialidad = ?
            WHERE id_veterinario = ?
        """
        parametros = (
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