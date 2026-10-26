class Pronostico:
    
    # Entidad de dominio que representa las condiciones climáticas de una comuna para planificar atenciones domiciliarias y alertar sobre bienestar animal.
    
    def __init__(self, ciudad: str, region: str, temperatura_c: float, condicion: str, humedad: int):
        self.ciudad = ciudad
        self.region = region
        self.temperatura_c = float(temperatura_c)
        self.condicion = condicion
        self.humedad = int(humedad)

    def alerta_golpe_de_calor(self) -> bool:

        # Regla de Negocio: Riesgo térmico para razas caninas braquicéfalas si temp > 30°C.
        return self.temperatura_c >= 30.0

    def es_riesgoso_para_terreno(self) -> bool:

        # Regla de Negocio: Alerta si hay precipitaciones o tormenta para visitas a parcelas.
        condicion_baja = self.condicion.lower()
        terminos_peligro = ["lluvia", "tormenta", "chubasco", "nieve", "granizo"]
        return any(termino in condicion_baja for termino in terminos_peligro)

    def __str__(self) -> str:
        alerta = " [RIESGO TÉRMICO]" if self.alerta_golpe_de_calor() else ""
        return f"[{self.ciudad}, {self.region}] {self.temperatura_c}°C - {self.condicion} (Humedad: {self.humedad}%){alerta}"

