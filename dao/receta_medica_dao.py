from database import ConexionDB
from models.especialidad import Especialidad
from models.receta_medica import RecetaMedica
from models.veterinario import Veterinario


class RecetaMedicaDAO:
    def __init__(self, conexion_db: ConexionDB):
        self._db = conexion_db
        self.crear_tabla()

    def crear_tabla(self):
        ddl = """
            CREATE TABLE IF NOT EXISTS receta_medica (
                id_receta INTEGER PRIMARY KEY,
                nombre_comercial TEXT NOT NULL,
                cantidad_mg INTEGER NOT NULL CHECK(cantidad_mg >= 0),
                instrucciones TEXT NOT NULL,
                id_veterinario INTEGER,
                FOREIGN KEY (id_veterinario) REFERENCES veterinarios(id_veterinario)
            )
        """
        with self._db.obtener_conexion() as conn:
            conn.execute(ddl)
            columnas = {
                fila[1] for fila in conn.execute("PRAGMA table_info(receta_medica)")
            }
            if "id_veterinario" not in columnas:
                conn.execute(
                    "ALTER TABLE receta_medica "
                    "ADD COLUMN id_veterinario INTEGER REFERENCES veterinarios(id_veterinario)"
                )

    def insertar(self, receta: RecetaMedica) -> None:
        veterinario = receta.veterinario
        if veterinario is None:
            raise ValueError("La receta médica debe tener un veterinario prescriptor.")
        sql = """
            INSERT INTO receta_medica (
                id_receta, nombre_comercial, cantidad_mg, instrucciones, id_veterinario
            )
            VALUES (?, ?, ?, ?, ?)
        """
        parametros = (
            receta.id_receta,
            receta.nombre_comercial,
            receta.cantidad_mg,
            receta.instrucciones,
            veterinario.id_veterinario,
        )
        with self._db.obtener_conexion() as conn:
            conn.execute(sql, parametros)

    def obtener_por_id_estricto(self, id_receta: int) -> RecetaMedica:
        sql = """
            SELECT r.id_receta, r.nombre_comercial, r.cantidad_mg, r.instrucciones,
                   v.id_veterinario, v.nombre, v.rut, v.telefono, v.especialidad
            FROM receta_medica AS r
            LEFT JOIN veterinarios AS v ON v.id_veterinario = r.id_veterinario
            WHERE r.id_receta = ?
        """
        with self._db.obtener_conexion() as conn:
            fila = conn.execute(sql, (id_receta,)).fetchone()
        if fila is None:
            raise ValueError(f"No existe la receta médica con ID {id_receta}.")
        # Tupla: datos de receta seguidos por los datos del veterinario, si existe.
        veterinario = None
        if fila[4] is not None:
            veterinario = Veterinario(
                fila[4],
                fila[5],
                fila[6],
                fila[7],
                Especialidad(fila[8]),
            )
        return RecetaMedica(
            fila[0],
            fila[1],
            fila[2],
            fila[3],
            veterinario,
        )

    def listar_todos(self) -> list[RecetaMedica]:
        sql = """
            SELECT r.id_receta, r.nombre_comercial, r.cantidad_mg, r.instrucciones,
                   v.id_veterinario, v.nombre, v.rut, v.telefono, v.especialidad
            FROM receta_medica AS r
            LEFT JOIN veterinarios AS v ON v.id_veterinario = r.id_veterinario
            ORDER BY r.nombre_comercial
        """
        recetas = []
        with self._db.obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            filas = cursor.fetchall()

            for fila in filas:
                # Tupla: datos de receta seguidos por los datos del veterinario, si existe.
                veterinario = None
                if fila[4] is not None:
                    veterinario = Veterinario(
                        fila[4],
                        fila[5],
                        fila[6],
                        fila[7],
                        Especialidad(fila[8]),
                    )
                receta = RecetaMedica(
                    fila[0],
                    fila[1],
                    fila[2],
                    fila[3],
                    veterinario,
                )
                recetas.append(receta)
        return recetas

    def actualizar(self, receta: RecetaMedica) -> bool:
        veterinario = receta.veterinario
        if veterinario is None:
            raise ValueError("La receta médica debe tener un veterinario prescriptor.")
        sql = """
            UPDATE receta_medica
            SET nombre_comercial = ?, cantidad_mg = ?, instrucciones = ?, id_veterinario = ?
            WHERE id_receta = ?
        """
        parametros = (
            receta.nombre_comercial,
            receta.cantidad_mg,
            receta.instrucciones,
            veterinario.id_veterinario,
            receta.id_receta,
        )
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, parametros)
            if cursor.rowcount == 0:
                raise ValueError(f"No existe la receta médica con ID {receta.id_receta}.")
        return True

    def eliminar(self, id_receta: int) -> bool:
        sql = "DELETE FROM receta_medica WHERE id_receta = ?"
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, (id_receta,))
            if cursor.rowcount == 0:
                raise ValueError(f"No existe la receta médica con ID {id_receta}.")
        return True