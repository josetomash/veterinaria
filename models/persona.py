class Persona:
    def __init__(self, id_persona: int, nombre: str, rut: str, telefono: str):
        self.id_persona = id_persona
        self.nombre = nombre
        self.__rut = ""
        self.__telefono = ""
        self.rut = rut
        self.telefono = telefono

    @property
    def rut(self) -> str:
        return self.__rut

    @rut.setter
    def rut(self, rut_new: str):
        if not isinstance(rut_new, str):
            raise TypeError("El RUT debe ser una cadena de texto.")
        rut_original = rut_new
        rut_new = rut_new.replace(".", "").replace("-", "").upper()
        if len(rut_new) < 8 or len(rut_new) > 9:
            raise ValueError("Cantidad de caracteres imposible, verifique bien el rut.")
        cuerpo = rut_new[:-1]
        dv = rut_new[-1]
        if not cuerpo.isdigit():
            raise ValueError("No se permite letras en el cuerpo del rut, verifique bien el rut.")
        suma = 0
        multiplicador = 2
        for digit in reversed(cuerpo):
            suma += int(digit) * multiplicador
            multiplicador += 1
            if multiplicador > 7:
                multiplicador = 2
        resto = 11 - (suma % 11)
        if resto == 11:
            dv_calculado = "0"
        elif resto == 10:
            dv_calculado = "K"
        else:
            dv_calculado = str(resto)
        if dv_calculado == dv:
            self.__rut = rut_original
        else:
            raise ValueError("Rut inválido, verifique bien el rut.")

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono_new: str):
        if not isinstance(telefono_new, str):
            raise TypeError("El teléfono debe ser una cadena de texto.")
        telefono_new = telefono_new.strip()
        identificador = telefono_new[:4]
        if identificador != "+569":
            raise ValueError("Número de teléfono no reconocido. Debe comenzar con +569.")
        elif len(telefono_new) != 12:
            raise ValueError("Cantidad de dígitos imposible, verifique bien el número telefónico ingresado.")
        self.__telefono = telefono_new

    def actualizar_telefono(self, nuevo_telefono: str):
        self.telefono = nuevo_telefono

    def __str__(self):
        return (
            f"ID: {self.id_persona}\n"
            f"Nombre: {self.nombre}\n"
            f"RUT: {self.rut}\n"
            f"Teléfono: {self.telefono}"
        )