from datetime import date, datetime, timezone
import math


class Dolar:
	def __init__(self, timestamp: date, valor_dolar: float, conversion_clp: float):
		if not isinstance(timestamp, date):
			raise TypeError("El timestamp del dólar debe ser una fecha válida.")
		if not isinstance(valor_dolar, (int, float)) or not math.isfinite(valor_dolar) or valor_dolar <= 0:
			raise ValueError("El valor del dólar debe ser un número positivo.")
		if not isinstance(conversion_clp, (int, float)) or not math.isfinite(conversion_clp) or conversion_clp <= 0:
			raise ValueError("La conversión a CLP debe ser un número positivo.")
		self.timestamp = timestamp
		self.valor_dolar = float(valor_dolar)
		self.conversion_clp = float(conversion_clp)

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
				timestamp = datetime.fromisoformat(fecha.replace("Z", "+00:00")).date()
		else:
			raise TypeError("El timestamp de la API tiene un formato no reconocido.")

		return cls(timestamp, 1.0, float(conversion))

	def __str__(self) -> str:
		return (
			f"Fecha: {self.timestamp.isoformat()} | "
			f"USD: {self.valor_dolar:.2f} | 1 USD = {self.conversion_clp:,.2f} CLP"
		)
