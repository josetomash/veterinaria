from datetime import date

from database import ConexionDB
from models.especie import Especie
from models.mascota import Mascota


class MascotaDAO:
    def __init__(self, conexion_db: ConexionDB):
        self._db = conexion_db
        self.crear_tabla()

    def crear_tabla(self):
        ddl = """
            CREATE TABLE IF NOT EXISTS mascotas (
                id_mascota INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                fecha_nacimiento TEXT NOT NULL,
                id_especie INTEGER NOT NULL,
                id_propietario INTEGER NOT NULL,
                FOREIGN KEY (id_especie) REFERENCES especies(id_especie),
                FOREIGN KEY (id_propietario) REFERENCES propietarios(id_propietario)
            )
        """
        with self._db.obtener_conexion() as conn:
            conn.execute(ddl)
            self._db.migrar_tabla_sin_autoincrement(conn, "mascotas")
            # Bases antiguas: cada mascota ahora guarda quién es su dueño
            columnas = {
                fila[1] for fila in conn.execute("PRAGMA table_info(mascotas)")
            }
            if "id_propietario" not in columnas:
                conn.execute(
                    "ALTER TABLE mascotas "
                    "ADD COLUMN id_propietario INTEGER REFERENCES propietarios(id_propietario)"
                )

    def insertar(self, mascota: Mascota) -> None:
        sql = """
            INSERT INTO mascotas (id_mascota, nombre, fecha_nacimiento, id_especie, id_propietario)
            VALUES (?, ?, ?, ?, ?)
        """
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
            mascota.id_propietario,
        )
        with self._db.obtener_conexion() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO especies (id_especie, nombre, informacion) VALUES (?, ?, ?)",
                parametros_especie,
            )
            cursor = conn.execute(sql, parametros_mascota)
            # La base de datos asigna el ID automáticamente
            mascota.id_mascota = cursor.lastrowid

    def _crear_mascota(self, fila) -> Mascota:
        # Tupla: (id_mascota, nombre, fecha_nacimiento, id_especie, id_propietario)
        especie = next(
            especie
            for especie in Especie
            if especie.id_especie == fila[3]
        )
        return Mascota(
            fila[0],
            fila[1],
            date.fromisoformat(fila[2]),
            especie,
            fila[4],
        )

    def obtener_por_id_estricto(self, id_mascota: int) -> Mascota:
        sql = "SELECT id_mascota, nombre, fecha_nacimiento, id_especie, id_propietario FROM mascotas WHERE id_mascota = ?"
        with self._db.obtener_conexion() as conn:
            fila = conn.execute(sql, (id_mascota,)).fetchone()
        if fila is None:
            raise ValueError(f"No existe la mascota con ID {id_mascota}.")
        return self._crear_mascota(fila)

    def listar_todos(self) -> list[Mascota]:
        sql = "SELECT id_mascota, nombre, fecha_nacimiento, id_especie, id_propietario FROM mascotas ORDER BY id_mascota"
        mascotas = []
        with self._db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()

            for fila in filas:
                # Tupla: (id_mascota, nombre, fecha_nacimiento, id_especie, id_propietario)
                especie = next(
                    especie
                    for especie in Especie
                    if especie.id_especie == fila[3]
                )
                mascota = Mascota(
                    fila[0],
                    fila[1],
                    date.fromisoformat(fila[2]),
                    especie,
                    fila[4],
                )
                mascotas.append(mascota)
        return mascotas

    def actualizar(self, mascota: Mascota) -> bool:
        sql = """
            UPDATE mascotas
            SET nombre = ?, fecha_nacimiento = ?, id_especie = ?
            WHERE id_mascota = ?
        """
        parametros = (
            mascota.nombre,
            mascota.fecha_nacimiento.isoformat(),
            mascota.especie.id_especie,
            mascota.id_mascota,
        )
        with self._db.obtener_conexion() as conn:
            conn.execute(
                "INSERT OR IGNORE INTO especies (id_especie, nombre, informacion) VALUES (?, ?, ?)",
                (
                    mascota.especie.id_especie,
                    mascota.especie.nombre_especie,
                    mascota.especie.informacion_especie,
                ),
            )
            cursor = conn.execute(sql, parametros)
            if cursor.rowcount == 0:
                raise ValueError(f"No existe la mascota con ID {mascota.id_mascota}.")
        return True

    def eliminar(self, id_mascota: int) -> bool:
        sql = "DELETE FROM mascotas WHERE id_mascota = ?"
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, (id_mascota,))
            if cursor.rowcount == 0:
                raise ValueError(f"No existe la mascota con ID {id_mascota}.")
        return True