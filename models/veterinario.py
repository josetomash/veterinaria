from persona import Persona

class Veterinario:
    def __init__(self, nombre:str, rut:str, telefono:str, id_veterinario:int):
        super().__init__(nombre, rut, telefono)#se añade los atributos de la clase padre

        #atributos especiales de la clase actual
        self.id_veterinario = id_veterinario

    