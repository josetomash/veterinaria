from datetime import date 
#Se importa el tipo de variable 'date' para las fechas

class Consulta:
    def __init__(self, id_consulta:int, motivo:str, fecha_consulta:date):

        #Atributos 
        self.id_consulta = id_consulta
        self.motivo= motivo

        #Atributos privados
        self.__fecha_consulta = None
        self.__fecha_consulta = fecha_consulta

    #filtro de fecha
    @property
    def fecha_consulta(self)-> date:
        return self.__fecha_consulta

    @fecha_consulta.setter
    def fecha_consulta(self, nueva_fecha:date):
        if not isinstance(nueva_fecha, date):
            raise TypeError(f"Usted debe de ingresar una fecha valida.")
        if nueva_fecha > date.today():
            raise ValueError(f"Fecha invalida. La fecha no puede ser mayor a la fecha actual. fecha recibida: {nueva_fecha}")
        if nueva_fecha < date(2000, 1, 1):
            raise ValueError(f"Fecha invalida. La fecha no puede ser menor a 01/01/200. fecha recibida: {nueva_fecha}")
        self.__fecha_consulta = nueva_fecha