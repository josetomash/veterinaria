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
                email TEXT NOT NULL,
                id_mascota INTEGER NOT NULL,
                FOREIGN KEY (id_mascota) REFERENCES mascotas(id_mascota)
            )
        """
        with self._db.obtener_conexion() as conn:
            conn.execute(ddl)
    
    def insertar(self, propietario: Propietario) -> None:
        sql_especie = """
            INSERT OR IGNORE INTO especies (id_especie, nombre, informacion)
            VALUES (?, ?, ?)
        """
        sql_mascota = """
            INSERT INTO mascotas (id_mascota, nombre, fecha_nacimiento, id_especie)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id_mascota) DO UPDATE SET
                nombre = excluded.nombre,
                fecha_nacimiento = excluded.fecha_nacimiento,
                id_especie = excluded.id_especie
        """
        sql = """
            INSERT INTO propietarios (
                id_propietario,
                nombre,
                rut,
                telefono,
                email,
                id_mascota
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """
        mascota = propietario.mascota
        parametros_especie = (
            mascota.especie.id_especie,
            mascota.especie.nombre_especie,
            mascota.especie.informacion_especie,
        )
        parametros_mascota = (
            mascota.id_mascota,
            mascota.nombre,
            mascota.fecha_nacimiento.isoformat(),
            mascota.especie.id_especie,
        )
        parametros = (
            propietario.id_propietario,
            propietario.nombre.strip(),
            propietario.rut.strip(),
            propietario.telefono.strip(),
            propietario.email.strip(),
            mascota.id_mascota,
        )
        with self._db.obtener_conexion() as conn:
            conn.execute(sql_especie, parametros_especie)
            conn.execute(sql_mascota, parametros_mascota)
            conn.execute(sql, parametros)

    def _crear_propietario(self, fila_propietario, fila_mascota) -> Propietario:
        # Tuplas:
        # fila_propietario=(id_propietario, nombre, rut, telefono, email, id_mascota);
        # fila_mascota=(id_mascota, nombre, fecha_nacimiento, id_especie)
        especie = next(
            especie
            for especie in Especie
            if especie.id_especie == fila_mascota[3]
        )
        mascota = Mascota(
            fila_mascota[0],
            fila_mascota[1],
            date.fromisoformat(fila_mascota[2]),
            especie,
        )
        return Propietario(
            fila_propietario[1],
            fila_propietario[2],
            fila_propietario[3],
            fila_propietario[0],
            fila_propietario[4],
            mascota,
        )

    def obtener_por_id_estricto(self, id_propietario: int) -> Propietario:
        sql_propietario = """
            SELECT id_propietario, nombre, rut, telefono, email, id_mascota
            FROM propietarios
            WHERE id_propietario = ?
        """
        sql_mascota = """
            SELECT id_mascota, nombre, fecha_nacimiento, id_especie
            FROM mascotas
            WHERE id_mascota = ?
        """
        with self._db.obtener_conexion() as conn:
            fila_propietario = conn.execute(sql_propietario, (id_propietario,)).fetchone()
            if fila_propietario is None:
                raise ValueError(f"No existe el propietario con ID {id_propietario}.")
            # Tupla: (id_propietario, nombre, rut, telefono, email, id_mascota)
            fila_mascota = conn.execute(sql_mascota, (fila_propietario[5],)).fetchone()
        if fila_mascota is None:
            raise ValueError(
                f"No se encontró la mascota asociada al propietario con ID {id_propietario}."
            )
        return self._crear_propietario(fila_propietario, fila_mascota)

    def listar_todos(self) -> list[Propietario]:
        sql_propietarios = """
            SELECT id_propietario, nombre, rut, telefono, email, id_mascota
            FROM propietarios
            ORDER BY nombre
        """
        sql_mascota = """
            SELECT id_mascota, nombre, fecha_nacimiento, id_especie
            FROM mascotas
            WHERE id_mascota = ?
        """
        propietarios = []
        with self._db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_propietarios)
            filas_propietarios = cursor.fetchall()

            for fila_propietario in filas_propietarios:
                # Tupla: (id_propietario, nombre, rut, telefono, email, id_mascota)
                cursor.execute(sql_mascota, (fila_propietario[5],))
                fila_mascota = cursor.fetchone()
                if fila_mascota is None:
                    raise ValueError(
                        "No se encontró la mascota asociada al propietario "
                        # Tupla fila_propietario: (id_propietario, nombre, rut, telefono, email, id_mascota)
                        f"con ID {fila_propietario[0]}."
                    )
                propietarios.append(self._crear_propietario(fila_propietario, fila_mascota))
        return propietarios

    def actualizar(self, propietario: Propietario) -> bool:
        sql = """
            UPDATE propietarios
            SET nombre = ?, rut = ?, telefono = ?, email = ?, id_mascota = ?
            WHERE id_propietario = ?
        """
        mascota = propietario.mascota
        with self._db.obtener_conexion() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO especies (id_especie, nombre, informacion) VALUES (?, ?, ?)",
                (
                    mascota.especie.id_especie,
                    mascota.especie.nombre_especie,
                    mascota.especie.informacion_especie,
                ),
            )
            conn.execute(
                """
                INSERT INTO mascotas (id_mascota, nombre, fecha_nacimiento, id_especie)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(id_mascota) DO UPDATE SET
                    nombre = excluded.nombre,
                    fecha_nacimiento = excluded.fecha_nacimiento,
                    id_especie = excluded.id_especie
                """,
                (
                    mascota.id_mascota,
                    mascota.nombre,
                    mascota.fecha_nacimiento.isoformat(),
                    mascota.especie.id_especie,
                ),
            )
            cursor = conn.execute(sql, (
                propietario.nombre,
                propietario.rut,
                propietario.telefono,
                propietario.email,
                mascota.id_mascota,
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