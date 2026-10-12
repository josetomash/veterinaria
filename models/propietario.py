from persona import Persona

class Propietario(Persona):
    def __init__(self, nombre:str, rut:str, telefono:str, id_propietario:int):
        super().__init__(nombre, rut, telefono)#se añade los atributos de la clase padre

        #atributos especiales de la clase actual
        self.id_propietario = id_propietario
        pass