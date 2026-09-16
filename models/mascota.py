from datetime import date 
#Se importa el tipo de variable 'date' para las fechas

class Mascota:
    def __init__(self, id_mascota:int, nombre:str, fecha_nacimiento:date):

        #Atributos 
        self.id_mascota = id_mascota
        self.nombre= nombre
        self.fecha_nacimiento = fecha_nacimiento