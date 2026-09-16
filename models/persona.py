class Persona:
    def __init__(self, id_persona:int, nombre:str, rut:str, telefono:str):

        #atributos
        self.id_persona = id_persona
        self.nombre = nombre

        #atributos privados
        self.__rut = ""
        self.__telefono = ""

        self.rut = rut
        self.telefono = telefono

    #filtro de rut
    @property
    def rut(self)-> str:
        return self.__rut

    @rut.setter
    def rut(self,):
        pass