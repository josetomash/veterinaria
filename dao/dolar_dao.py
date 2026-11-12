from datetime import date

from database import ConexionDB
from models.dolar import Dolar


class DolarDAO:
	def __init__(self, conexion_db: ConexionDB):
		self._db = conexion_db
		self.crear_tabla()
	# llamado desde el constructor

	# IMPORTANTE: REAL es un tipo de dato numerico de punto flotante de precision simple 
	# guarda numeros decimales de forma aproximada
	# Precision: Ofrece una precision de aproximadamente 7 digitos decimales. 
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
	# llamado desde service
	def obtener_ultima(self) -> Dolar | None:
		sql = """
			SELECT timestamp, valor_dolar, conversion_clp
			FROM dolar
			ORDER BY timestamp DESC, id_dolar DESC
			LIMIT 1
		"""
		# limit 1 permite obtener el registro mas actual
		# fetchone devuelve la fila 
		# fetchall devuelve todas las filas que pillo en consulta
		with self._db.obtener_conexion() as conn:
			fila = conn.execute(sql).fetchone()
		if fila is None:
			return None
		# fila[0]: fromisoformat (texto a fecha)
		# fila[1]: valor_dolar (num)
		# fila[2]: conversion_clp (num)
		return Dolar(date.fromisoformat(fila[0]), fila[1], fila[2])
	# llamado desde service
	def guardar(self, dolar: Dolar) -> None:
		sql = """
			INSERT INTO dolar (timestamp, valor_dolar, conversion_clp)
			VALUES (?, ?, ?)
		"""
		with self._db.obtener_conexion() as conn:
			# isoformat() fecha a texto
			# lo demas. son numeros
			conn.execute(
				sql,
				(dolar.timestamp.isoformat(), dolar.valor_dolar, dolar.conversion_clp),
			)
