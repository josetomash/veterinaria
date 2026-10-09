from database import ConexionDB
from models.medicamento import Medicamento


class MedicamentoDAO:
    def __init__(self, conexion_db: ConexionDB):
        self._db = conexion_db
        self.crear_tabla()

    def crear_tabla(self):
        ddl = """
            CREATE TABLE IF NOT EXISTS medicamentos (
                id_medicamento INTEGER PRIMARY KEY,
                nombre_comercial TEXT NOT NULL UNIQUE,
                nombre_generico TEXT NOT NULL,
                tipo TEXT NOT NULL,
                precio REAL NOT NULL CHECK(precio > 0),
                stock INTEGER NOT NULL CHECK(stock >= 0)
            )
        """
        with self._db.obtener_conexion() as conn:
            conn.execute(ddl)

    def insertar(self, medicamento: Medicamento) -> None:
        sql = """
            INSERT INTO medicamentos (
                id_medicamento, nombre_comercial, nombre_generico, tipo, precio, stock
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """
        parametros = (
            medicamento.id_medicamento,
            medicamento.nombre_comercial,
            medicamento.nombre_generico,
            medicamento.tipo,
            medicamento.precio,
            medicamento.stock,
        )
        with self._db.obtener_conexion() as conn:
            conn.execute(sql, parametros)

    def obtener_por_id_estricto(self, id_medicamento: int) -> Medicamento:
        sql = """
            SELECT id_medicamento, nombre_comercial, nombre_generico, tipo, precio, stock
            FROM medicamentos
            WHERE id_medicamento = ?
        """
        with self._db.obtener_conexion() as conn:
            fila = conn.execute(sql, (id_medicamento,)).fetchone()
        if fila is None:
            raise ValueError(f"No existe el medicamento con ID {id_medicamento}.")
        return Medicamento(*fila)

    def listar_todos(self) -> list[Medicamento]:
        sql = """
            SELECT id_medicamento, nombre_comercial, nombre_generico, tipo, precio, stock
            FROM medicamentos
            ORDER BY nombre_comercial
        """
        with self._db.obtener_conexion() as conn:
            filas = conn.execute(sql).fetchall()
        return [Medicamento(*fila) for fila in filas]

    def buscar_por_termino_seguro(self, termino: str) -> list[Medicamento]:
        sql = """
            SELECT id_medicamento, nombre_comercial, nombre_generico, tipo, precio, stock
            FROM medicamentos
            WHERE nombre_comercial LIKE ?
            ORDER BY nombre_comercial
        """
        with self._db.obtener_conexion() as conn:
            filas = conn.execute(sql, (f"%{termino}%",)).fetchall()
        return [Medicamento(*fila) for fila in filas]

    def actualizar(self, medicamento: Medicamento) -> bool:
        sql = """
            UPDATE medicamentos
            SET nombre_comercial = ?, nombre_generico = ?, tipo = ?, precio = ?, stock = ?
            WHERE id_medicamento = ?
        """
        parametros = (
            medicamento.nombre_comercial,
            medicamento.nombre_generico,
            medicamento.tipo,
            medicamento.precio,
            medicamento.stock,
            medicamento.id_medicamento,
        )
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, parametros)
            if cursor.rowcount == 0:
                raise ValueError(f"No existe el medicamento con ID {medicamento.id_medicamento}.")
        return True

    def eliminar(self, id_medicamento: int) -> bool:
        sql = "DELETE FROM medicamentos WHERE id_medicamento = ?"
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, (id_medicamento,))
            if cursor.rowcount == 0:
                raise ValueError(f"No existe el medicamento con ID {id_medicamento}.")
        return True

    def actualizar_stock_seguro(self, id_medicamento: int, nuevo_stock: int) -> bool:
        sql = "UPDATE medicamentos SET stock = ? WHERE id_medicamento = ?"
        with self._db.obtener_conexion() as conn:
            cursor = conn.execute(sql, (nuevo_stock, id_medicamento))
            if cursor.rowcount == 0:
                raise ValueError(f"No existe el medicamento con ID {id_medicamento}.")
        return True