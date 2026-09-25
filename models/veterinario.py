from persona import Persona
from especialidad import Especialidad


class Veterinario(Persona):
    def __init__(self, id_persona: int, nombre: str, rut: str, telefono: str, id_veterinario: int, especialidad: Especialidad):
        super().__init__(id_persona, nombre, rut, telefono)
        self.id_veterinario = id_veterinario
        self.especialidad = especialidad

    @property
    def especialidad(self):
        return self._especialidad

    @especialidad.setter
    def especialidad(self, nueva_especialidad: Especialidad):
        if not isinstance(nueva_especialidad, Especialidad):
            raise TypeError("La especialidad debe ser una instancia de la clase Especialidad.")
        self._especialidad = nueva_especialidad

    def realizar_consulta(self):
        pass

    def __str__(self):
        return (
            f"{super().__str__()}\n"
            f"ID Veterinario: {self.id_veterinario}\n"
            f"Especialidad: {self.especialidad.value.strip()}"
        )