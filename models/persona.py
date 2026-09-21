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
        #añadir una funcion la cual filtre los datos de entrada de los ruts !!
        pass


    #filtro de telefono
    @property
    def telefono(self)-> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono:str):
        # Lógica para filtrar el teléfono
        pass