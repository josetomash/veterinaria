from abc import ABC, abstractmethod   #Para transformar la clase en una abstracta
from exceptions import RutInvalidoException, TelefonoInvalidoException #Para saber que tipo de error es
class Persona(ABC):
    def __init__(self, nombre:str, rut:str, telefono:str):
        #atributos privados
        self.__nombre = ""
        self.__rut = ""
        self.__telefono = ""

        self.nombre = nombre
        self.rut = rut
        self.telefono = telefono

    #---------------------------------------------------------------------------------------
    # FILTROS (PROPERTY Y SETTER)
    #---------------------------------------------------------------------------------------

    #FILTRO DE NOMBRE
    @property
    def nombre(self)-> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre_nuevo: str):
        if not isinstance(nombre_nuevo, str) or not nombre_nuevo.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self.__nombre = " ".join(nombre_nuevo.split()).title()

    #FILTRO DE RUT
    @property
    def rut(self)-> str:
        return self.__rut

    @rut.setter
    def rut(self,rut_new:str):
        rut_new_original =  rut_new.replace(".", "").upper().strip()
        rut_new = rut_new.replace(".", "").replace("-", "").upper().strip()

        if len(rut_new) < 8 or len(rut_new) > 9:
            raise RutInvalidoException("cantidad de caracteres imposible, verifique bien el rut")
        
        cuerpo = rut_new[:-1]
        dv = rut_new[-1]

        if not cuerpo.isdigit():
            raise RutInvalidoException("No se permite letras en el cuerpo del rut, verifique bien el rut")
        
        suma = 0
        multiplicador = 2
        for digit in reversed(cuerpo):
            suma += int(digit) * multiplicador
            multiplicador += 1
            if multiplicador > 7:
                multiplicador = 2

        resto = 11 - (suma % 11)

        if resto == 11:
            dv_calculado = 0
        elif resto == 10:
            dv_calculado = "K"
        else:
            dv_calculado = resto

        if dv_calculado == dv:
            self.__rut = rut_new_original
        else:
            raise RutInvalidoException("Rut invalido, verifique bien el rut")

    #FILTRO DE TELEFONO
    @property
    def telefono(self)-> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono_new:str):
        digitos = "".join(caracter for caracter in telefono_new if caracter.isdigit())
        if len(digitos) == 11 and digitos.startswith("56"):
            digitos = digitos[2:]
        if len(digitos) != 9 or not digitos.startswith("9"):
            raise TelefonoInvalidoException(
                f"Teléfono '{telefono_new}' inválido. Use un celular chileno, ej: 9 1234 5678."
            )
        self.__telefono = "+56 {digitos[0]} {digitos[1:5]} {digitos[5:]}"

    # ------------------------------------------------------------------
    # MÉTODOS ABSTRACTOS
    # ------------------------------------------------------------------

    @abstractmethod
    def obtener_rol(self) -> str:
        pass

    # ------------------------------------------------------------------
    # MÉTODOS
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return f"[{self.obtener_rol()}] {self.nombre} | RUT {self.rut} | Tel {self.telefono}"