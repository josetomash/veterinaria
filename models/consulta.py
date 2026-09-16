from datetime import date 
#Se importa el tipo de variable 'date' para las fechas

class Consulta:
    def __init__(self, id_consulta:int, motivo:str, fecha_consulta:date):

        #Atributos 
        self.id_consulta = id_consulta
        self.motivo= motivo
        self.fecha_consulta = fecha_consulta