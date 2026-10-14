from datetime import date

from database import ConexionDB
from models.especie import Especie
from models.mascota import Mascota
from models.propietario import Propietario


class PropietarioDAO:
    def __init__(self, conexion_db: ConexionDB):
        self._db = conexion_db
        self.crear_tabla()

    def crear_tabla(self):
        ddl = """
            CREATE TABLE IF NOT EXISTS propietarios (
                id_propietario INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                rut TEXT NOT NULL UNIQUE,
                telefono TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """
        with self._db.obtener_conexion() as conn:
            conn.execute(ddl)
            columnas = {
                fila[1] for fila in conn.execute("PRAGMA table_info(propietarios)")
            }
            if "id_mascota" in columnas:
                self._migrar_relacion_mascotas(conn)
            else:
                self._db.migrar_tabla_sin_autoincrement(conn, "propietarios")

    def _migrar_relacion_mascotas(self, conn):
        # Bases antiguas: el propietario guardaba UNA mascota (id_mascota).
        # Ahora cada mascota guarda a su dueño (mascotas.id_propietario),
        # así un propietario puede tener varias mascotas.
        conn.execute("PRAGMA foreign_keys = OFF")
        columnas_mascotas = {
            fila[1] for fila in conn.execute("PRAGMA table_info(mascotas)")
        }
        if "id_propietario" not in columnas_mascotas:
            conn.execute(
                "ALTER TABLE mascotas "
                "ADD COLUMN id_propietario INTEGER REFERENCES propietarios(id_propietario)"
            )
        conn.execute(
            """
            UPDATE mascotas
            SET id_propietario = (
                SELECT id_propietario FROM propietarios
                WHERE propietarios.id_mascota = mascotas.id_mascota
            )
            WHERE id_propietario IS NULL
            """
        )
        # Se rehace la tabla propietarios sin la columna id_mascota
        conn.execute(
            """
            CREATE TABLE propietarios_nueva (
                id_propietario INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                rut TEXT NOT NULL UNIQUE,
                telefono TEXT NOT NULL,
                email TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            INSERT INTO propietarios_nueva (id_propietario, nombre, rut, telefono, email)
            SELECT id_propietario, nombre, rut, telefono, email FROM propietarios
            """
        )
        conn.execute("DROP TABLE propietarios")
        conn.execute("ALTER TABLE propietarios_nueva RENAME TO propietarios")

    def insertar(self, propietario: Propietario) -> None:
        sql = """
            INSERT INTO propietarios (
                id_propietario,
                nombre,
                rut,
                telefono,
                email
            )
            VALUES (?, ?, ?, ?, ?)
        """
        sql_especie = """
            INSERT OR IGNORE INTO especies (id_especie, nombre, informacion)
            VALUES (?, ?, ?)
        """
        sql_mascota = """
            INSERT INTO mascotas (id_mascota, nombre, fecha_nacimiento, id_especie, id_propietario)
            VALUES (?, ?, ?, ?, ?)
        """
        parametros = (
            propietario.id_propietario,
            propietario.nombre.strip(),
            propietario.rut.strip(),
            propietario.telefono.strip(),
            propietario.email.strip(),
        )
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, parametros)
            # La base de datos asigna el ID automáticamente
            propietario.id_propietario = cursor.lastrowid
            # Se guardan también las mascotas que trae el propietario
            for mascota in propietario.mascotas:
                mascota.id_propietario = propietario.id_propietario
                conn.execute(
                    sql_especie,
                    (
                        mascota.especie.id_especie,
                        mascota.especie.nombre_especie,
                        mascota.especie.informacion_especie,
                    ),
                )
                cursor = conn.execute(
                    sql_mascota,
                    (
                        mascota.id_mascota,
                        mascota.nombre,
                        mascota.fecha_nacimiento.isoformat(),
                        mascota.especie.id_especie,
                        mascota.id_propietario,
                    ),
                )
                mascota.id_mascota = cursor.lastrowid

    def _crear_propietario(self, fila_propietario, filas_mascotas) -> Propietario:
        # Tuplas:
        # fila_propietario=(id_propietario, nombre, rut, telefono, email);
        # filas_mascotas=[(id_mascota, nombre, fecha_nacimiento, id_especie, id_propietario), ...]
        mascotas = []
        for fila_mascota in filas_mascotas:
            especie = next(
                especie
                for especie in Especie
                if especie.id_especie == fila_mascota[3]
            )
            mascotas.append(
                Mascota(
                    fila_mascota[0],
                    fila_mascota[1],
                    date.fromisoformat(fila_mascota[2]),
                    especie,
                    fila_mascota[4],
                )
            )
        return Propietario(
            fila_propietario[1],
            fila_propietario[2],
            fila_propietario[3],
            fila_propietario[0],
            fila_propietario[4],
            mascotas,
        )

    def obtener_por_id_estricto(self, id_propietario: int) -> Propietario:
        sql_propietario = """
            SELECT id_propietario, nombre, rut, telefono, email
            FROM propietarios
            WHERE id_propietario = ?
        """
        sql_mascotas = """
            SELECT id_mascota, nombre, fecha_nacimiento, id_especie, id_propietario
            FROM mascotas
            WHERE id_propietario = ?
            ORDER BY id_mascota
        """
        with self._db.obtener_conexion() as conn:
            fila_propietario = conn.execute(sql_propietario, (id_propietario,)).fetchone()
            if fila_propietario is None:
                raise ValueError(f"No existe el propietario con ID {id_propietario}.")
            # Tupla: (id_propietario, nombre, rut, telefono, email)
            filas_mascotas = conn.execute(sql_mascotas, (fila_propietario[0],)).fetchall()
        return self._crear_propietario(fila_propietario, filas_mascotas)

    def listar_todos(self) -> list[Propietario]:
        sql_propietarios = """
            SELECT id_propietario, nombre, rut, telefono, email
            FROM propietarios
            ORDER BY id_propietario
        """
        sql_mascotas = """
            SELECT id_mascota, nombre, fecha_nacimiento, id_especie, id_propietario
            FROM mascotas
            WHERE id_propietario = ?
            ORDER BY id_mascota
        """
        propietarios = []
        with self._db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_propietarios)
            filas_propietarios = cursor.fetchall()

            for fila_propietario in filas_propietarios:
                # Tupla: (id_propietario, nombre, rut, telefono, email)
                cursor.execute(sql_mascotas, (fila_propietario[0],))
                filas_mascotas = cursor.fetchall()
                propietarios.append(self._crear_propietario(fila_propietario, filas_mascotas))
        return propietarios

    def actualizar(self, propietario: Propietario) -> bool:
        # Solo se actualizan los datos del propietario.
        # Sus mascotas se actualizan desde la opción "Actualizar mascota".
        sql = """
            UPDATE propietarios
            SET nombre = ?, rut = ?, telefono = ?, email = ?
            WHERE id_propietario = ?
        """
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, (
                propietario.nombre,
                propietario.rut,
                propietario.telefono,
                propietario.email,
                propietario.id_propietario,
            ))
            if cursor.rowcount == 0:
                raise ValueError(f"No existe el propietario con ID {propietario.id_propietario}.")
        return True

    def eliminar(self, id_propietario: int) -> bool:
        sql = "DELETE FROM propietarios WHERE id_propietario = ?"
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, (id_propietario,))
            if cursor.rowcount == 0:
                raise ValueError(f"No existe el propietario con ID {id_propietario}.")
        return True
