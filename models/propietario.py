from .persona import Persona
from .mascota import Mascota


class Propietario(Persona):
    def __init__(
        self, 
        nombre: str, 
        rut: str, 
        telefono: str, 
        id_propietario: int, 
        email: str, 
        mascotas: list[Mascota]
    ):
        super().__init__(nombre, rut, telefono)
        self.id_propietario = id_propietario
        self.email = email
        self.mascotas = mascotas

    @property
    def id_propietario(self) -> int:
        return self._id_propietario

    @id_propietario.setter
    def id_propietario(self, nuevo_id: int | None):
        if nuevo_id is None:
            # Aún no se guarda: el ID lo asigna la base de datos (AUTOINCREMENT)
            self._id_propietario = None
            return
        if not isinstance(nuevo_id, int) or isinstance(nuevo_id, bool):
            raise TypeError("El ID del propietario debe ser un número entero.")
        if nuevo_id <= 0:
            raise ValueError("El ID del propietario debe ser un número positivo.")
        self._id_propietario = nuevo_id

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, nuevo_email: str):
        if not isinstance(nuevo_email, str):
            raise TypeError("El email debe ser una cadena de texto.")
        if not nuevo_email.strip():
            raise ValueError("El email no puede estar vacío.")
        if "@" not in nuevo_email:
            raise ValueError("El formato del email no es válido (debe contener '@').")
        self._email = nuevo_email.strip()

    @property
    def mascotas(self) -> list[Mascota]:
        return self._mascotas

    @mascotas.setter
    def mascotas(self, nuevas_mascotas: list[Mascota]):
        if not isinstance(nuevas_mascotas, list):
            raise TypeError("Las mascotas deben entregarse en una lista.")
        for mascota in nuevas_mascotas:
            if not isinstance(mascota, Mascota):
                raise TypeError("Cada mascota debe ser una instancia de la clase Mascota.")
        self._mascotas = list(nuevas_mascotas)

    def asignar_mascota(self, nueva_mascota: Mascota):
        if not isinstance(nueva_mascota, Mascota):
            raise TypeError("La mascota debe ser una instancia de la clase Mascota.")
        self._mascotas.append(nueva_mascota)

    def __str__(self):
        return (
            f"{super().__str__()}\n"
            f"ID Propietario: {self.id_propietario}\n"
            f"Email: {self.email}\n"
            f"Mascotas: {', '.join(mascota.nombre for mascota in self.mascotas) or 'Sin mascotas'}"
        )
