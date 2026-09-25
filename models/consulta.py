from datetime import date

FECHA_MINIMA_CONSULTA = date(2000, 1, 1)


class Consulta:
    def __init__(self, id_consulta: int, motivo: str, fecha_consulta: date):
        self.id_consulta = id_consulta
        self.motivo = motivo
        self.__fecha_consulta = None
        self.__fecha_consulta = fecha_consulta

    @property
    def fecha_consulta(self) -> date:
        return self.__fecha_consulta

    @fecha_consulta.setter
    def fecha_consulta(self, nueva_fecha: date):
        if not isinstance(nueva_fecha, date):
            raise TypeError("Usted debe de ingresar una fecha válida.")
        if nueva_fecha > date.today():
            raise ValueError(f"Fecha inválida. La fecha no puede ser mayor a la fecha actual. Fecha recibida: {nueva_fecha}")
        if nueva_fecha < FECHA_MINIMA_CONSULTA:
            raise ValueError(f"Fecha inválida. La fecha no puede ser menor a {FECHA_MINIMA_CONSULTA.strftime('%d/%m/%Y')}. Fecha recibida: {nueva_fecha}")
        self.__fecha_consulta = nueva_fecha