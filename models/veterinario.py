from .persona import Persona
from .especialidad import Especialidad


class Veterinario(Persona):
    def __init__(
        self, 
        id_persona: int, 
        nombre: str, 
        rut: str, 
        telefono: str, 
        id_veterinario: int, 
        especialidad: Especialidad
    ):
        super().__init__(nombre, rut, telefono)
        self.id_persona = id_persona
        self.id_veterinario = id_veterinario
        self.especialidad = especialidad

    @property
    def id_persona(self) -> int:
        return self._id_persona

    @id_persona.setter
    def id_persona(self, nuevo_id: int):
        if not isinstance(nuevo_id, int) or isinstance(nuevo_id, bool):
            raise TypeError("El ID de la persona debe ser un número entero.")
        if nuevo_id <= 0:
            raise ValueError("El ID de la persona debe ser un número positivo.")
        self._id_persona = nuevo_id

    @property
    def id_veterinario(self) -> int:
        return self._id_veterinario

    @id_veterinario.setter
    def id_veterinario(self, nuevo_id: int):
        if not isinstance(nuevo_id, int) or isinstance(nuevo_id, bool):
            raise TypeError("El ID del veterinario debe ser un número entero.")
        if nuevo_id <= 0:
            raise ValueError("El ID del veterinario debe ser un número positivo mayor a 0.")
        self._id_veterinario = nuevo_id

    @property
    def especialidad(self) -> Especialidad:
        return self._especialidad

    @especialidad.setter
    def especialidad(self, nueva_especialidad: Especialidad):
        if not isinstance(nueva_especialidad, Especialidad):
            raise TypeError("La especialidad debe ser una instancia de la clase Especialidad.")
        self._especialidad = nueva_especialidad

    def realizar_consulta(self):
        pass

    def __str__(self) -> str:
        return (
            f"{super().__str__()}\n"
            f"ID Veterinario: {self.id_veterinario}\n"
            f"Especialidad: {self.especialidad.value.strip()}"
        )