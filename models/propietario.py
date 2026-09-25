from persona import Persona
from mascota import Mascota


class Propietario(Persona):
    def __init__(self, id_persona: int, nombre: str, rut: str, telefono: str, id_propietario: int, email: str, nombre_email: str, mascota: Mascota):
        super().__init__(id_persona, nombre, rut, telefono)
        self.id_propietario = id_propietario
        self.email = email
        self.nombre_email = nombre_email
        self._mascota = mascota

    @property
    def mascota(self):
        return self._mascota

    @mascota.setter
    def mascota(self, nueva_mascota: Mascota):
        if not isinstance(nueva_mascota, Mascota):
            raise TypeError("La mascota debe ser una instancia de la clase Mascota.")
        self._mascota = nueva_mascota

    def asignar_mascota(self, nueva_mascota: Mascota):
        self.mascota = nueva_mascota

    def __str__(self):
        return (
            f"{super().__str__()}\n"
            f"ID Propietario: {self.id_propietario}\n"
            f"Email: {self.email}\n"
            f"Nombre Email: {self.nombre_email}\n"
            f"Mascota: {self._mascota.nombre if self._mascota else 'Sin mascota'}"
        )