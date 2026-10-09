from datetime import date 
from .especie import Especie

class Mascota:
    def __init__(self, id_mascota: int, nombre: str, fecha_nacimiento: date, especie: Especie):
        self.id_mascota = id_mascota
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.especie = especie

    @property
    def id_mascota(self) -> int:
        return self._id_mascota

    @id_mascota.setter
    def id_mascota(self, nuevo_id: int):
        if not isinstance(nuevo_id, int) or isinstance(nuevo_id, bool):
            raise TypeError("El ID de la mascota debe ser un número entero.")
        if nuevo_id <= 0:
            raise ValueError("El ID de la mascota debe ser un número positivo.")
        self._id_mascota = nuevo_id

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        if not isinstance(nuevo_nombre, str):
            raise TypeError("El nombre debe ser una cadena de texto.")
        if not nuevo_nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = nuevo_nombre.strip()

    @property
    def fecha_nacimiento(self) -> date:
        return self._fecha_nacimiento

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, nueva_fecha: date):
        if not isinstance(nueva_fecha, date):
            raise TypeError("La fecha de nacimiento debe ser un objeto de tipo date.")
        if nueva_fecha > date.today():
            raise ValueError("La fecha de nacimiento no puede ser en el futuro.")
        self._fecha_nacimiento = nueva_fecha

    @property
    def especie(self) -> Especie:
        return self._especie

    @especie.setter
    def especie(self, nueva_especie: Especie):
        if not isinstance(nueva_especie, Especie):
            raise TypeError("La especie debe ser una instancia de la clase Especie.")
        self._especie = nueva_especie

    @property
    def tipo_especie(self) -> str:
        """Devuelve dinámicamente el tipo_especie desde el objeto Especie asociado."""
        return self.especie.nombre_especie

    def calcular_edad(self) -> int:
        """Calcula la edad de la mascota en años a partir de su fecha de nacimiento."""
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year
        if (hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day):
            edad -= 1
        return edad

    def __str__(self) -> str:
        return (
            f"ID Mascota: {self.id_mascota}\n"
            f"Nombre: {self.nombre}\n"
            f"Fecha de Nacimiento: {self.fecha_nacimiento.strftime('%d/%m/%Y')}\n"
            f"Especie: {self.tipo_especie}\n"
            f"Edad: {self.calcular_edad()} años"
        )