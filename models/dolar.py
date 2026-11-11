from datetime import date, datetime, timezone
import math


class Dolar:
	def __init__(self, timestamp: date, valor_dolar: float, conversion_clp: float):
		self.timestamp = timestamp
		self.valor_dolar = valor_dolar
		self.conversion_clp = conversion_clp

	@property
	def timestamp(self) -> date:
		return self._timestamp

	@timestamp.setter
	def timestamp(self, timestamp: date) -> None:
		if not isinstance(timestamp, date):
			raise TypeError("El timestamp del dolar debe ser una fecha valida.")

		self._timestamp = timestamp

	@property
	def valor_dolar(self) -> float:
		return self._valor_dolar

	@valor_dolar.setter
	def valor_dolar(self, valor_dolar: float) -> None:
		# comprobar que el numero sea finito con:
		# or not math.isfinite(conversion_clp)
		# con eso rechaza si no es un numero finito
		if not isinstance(valor_dolar, (int, float)) or not math.isfinite(valor_dolar) or valor_dolar <= 0:
			raise ValueError("El valor del dolar debe ser un número positivo.")

		self._valor_dolar = float(valor_dolar)

	@property
	def conversion_clp(self) -> float:
		return self._conversion_clp

	@conversion_clp.setter
	def conversion_clp(self, conversion_clp: float) -> None:
		# comprobar que el numero sea finito con:
		# or not math.isfinite(conversion_clp)
		# con eso rechaza si no es un numero finito
		if not isinstance(conversion_clp, (int, float)) or not math.isfinite(conversion_clp) or conversion_clp <= 0:
			raise ValueError("La conversion a CLP debe ser un número positivo.")

		self._conversion_clp = float(conversion_clp)

	@classmethod
	def limpiar_respuesta(cls, fuente: str, respuesta: dict) -> "Dolar":
		if not isinstance(respuesta, dict):
			raise TypeError("La respuesta de la API debe ser un objeto JSON.")

		if fuente == "exchangerate-api":
			fecha = respuesta.get("date")
			base = respuesta.get("base", "USD")
			tasas = respuesta.get("rates", {})
			conversion = tasas.get("CLP") if isinstance(tasas, dict) else None
		elif fuente == "open-er-api":
			fecha = respuesta.get("time_last_update_unix")
			if fecha is None:
				fecha = respuesta.get("time_last_update_utc")
			base = respuesta.get("base_code")
			tasas = respuesta.get("rates", {})
			conversion = tasas.get("CLP") if isinstance(tasas, dict) else None
		elif fuente == "frankfurter":
			fecha = respuesta.get("date")
			base = respuesta.get("base")
			tasas = respuesta.get("rates", {})
			conversion = tasas.get("CLP") if isinstance(tasas, dict) else None
		elif fuente == "currency-api":
			fecha = respuesta.get("date")
			base = "USD"
			dolares = respuesta.get("usd", {})
			conversion = dolares.get("clp") if isinstance(dolares, dict) else None
		else:
			raise ValueError(f"Fuente de cotización no soportada: {fuente}.")

		if base != "USD" or fecha is None or conversion is None:
			raise ValueError("La API no entregó timestamp, USD base y conversión a CLP.")

		if isinstance(fecha, (int, float)):
			timestamp = datetime.fromtimestamp(fecha, timezone.utc).date()
		elif isinstance(fecha, str):
			try:
				timestamp = date.fromisoformat(fecha[:10])
			except ValueError:
				# Z indica que la hora esta expresada en UTC (tiempo universal coordinado). Una ref mundial.
				# +00:00 representa la misma zona horaria con su desfase.
				# En python 3.9 si no se pone +00:00
				# ValueError: Invalid isoformat string: '2023-06-01T00:00:00Z'
				fecha_con_zona_horaria = fecha.replace("Z", "+00:00")
				fecha_hora = datetime.fromisoformat(fecha_con_zona_horaria)
				timestamp = fecha_hora.date()
		else:
			raise TypeError("El timestamp de la API tiene un formato no reconocido.")

		valor_dolar = 1.0
		conversion_clp = float(conversion)
		return cls(timestamp, valor_dolar, conversion_clp)

	def __str__(self) -> str:
		return (
			# isoformat() convierte objeto date a texto
			f"Fecha: {self.timestamp.isoformat()} | "
			# formato decimal con dos cifras despues del punto
			f"USD: {self.valor_dolar:.2f} | 1 USD = {self.conversion_clp:,.2f} CLP"
		)
