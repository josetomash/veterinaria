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

    def _crear_propietario(self, fila) -> Propietario:
        especie = next(especie for especie in Especie if especie.id_especie == fila[8])
        mascota = Mascota(fila[5], fila[6], date.fromisoformat(fila[7]), especie)
        return Propietario(fila[1], fila[2], fila[3], fila[0], fila[4], mascota)

    def obtener_por_id_estricto(self, id_propietario: int) -> Propietario:
        sql = """
            SELECT p.id_propietario, p.nombre, p.rut, p.telefono, p.email,
                   m.id_mascota, m.nombre, m.fecha_nacimiento, m.id_especie
            FROM propietarios AS p
            JOIN mascotas AS m ON m.id_mascota = p.id_mascota
            WHERE p.id_propietario = ?
        """
        with self._db.obtener_conexion() as conn:
            fila = conn.execute(sql, (id_propietario,)).fetchone()
        if fila is None:
            raise ValueError(f"No existe el propietario con ID {id_propietario}.")
        return self._crear_propietario(fila)

    def listar_todos(self) -> list[Propietario]:
        sql = """
            SELECT p.id_propietario, p.nombre, p.rut, p.telefono, p.email,
                   m.id_mascota, m.nombre, m.fecha_nacimiento, m.id_especie
            FROM propietarios AS p
            JOIN mascotas AS m ON m.id_mascota = p.id_mascota
            ORDER BY p.nombre
        """
        with self._db.obtener_conexion() as conn:
            filas = conn.execute(sql).fetchall()
        return [self._crear_propietario(fila) for fila in filas]

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