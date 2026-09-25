from datetime import date 
from especie import Especie
#Se importa el tipo de variable 'date' para las fechas

class Mascota:
    def __init__(self, id_mascota:int, nombre:str, fecha_nacimiento:date, especie:Especie):

        self.id_mascota = id_mascota
        self.nombre= nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.tipo_especie = especie.tipo_especie

    def calcular_edad(self) -> int:
        """Calcula la edad de la mascota en años a partir de su fecha de nacimiento."""
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad