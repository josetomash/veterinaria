from datetime import date

from database import ConexionDB
from models.dolar import Dolar


class DolarDAO:
	def __init__(self, conexion_db: ConexionDB):
		self._db = conexion_db
		self.crear_tabla()

	def crear_tabla(self) -> None:
		ddl = """
			CREATE TABLE IF NOT EXISTS dolar (
				id_dolar INTEGER PRIMARY KEY AUTOINCREMENT,
				timestamp DATE NOT NULL,
				valor_dolar REAL NOT NULL CHECK(valor_dolar > 0),
				conversion_clp REAL NOT NULL CHECK(conversion_clp > 0)
			)
		"""
		with self._db.obtener_conexion() as conn:
			conn.execute(ddl)

	def obtener_ultima(self) -> Dolar | None:
		sql = """
			SELECT timestamp, valor_dolar, conversion_clp
			FROM dolar
			ORDER BY timestamp DESC, id_dolar DESC
			LIMIT 1
		"""
		with self._db.obtener_conexion() as conn:
			fila = conn.execute(sql).fetchone()
		if fila is None:
			return None
		return Dolar(date.fromisoformat(fila[0]), fila[1], fila[2])

	def guardar(self, dolar: Dolar) -> None:
		sql = """
			INSERT INTO dolar (timestamp, valor_dolar, conversion_clp)
			VALUES (?, ?, ?)
		"""
		with self._db.obtener_conexion() as conn:
			conn.execute(
				sql,
				(dolar.timestamp.isoformat(), dolar.valor_dolar, dolar.conversion_clp),
			)
