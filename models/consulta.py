from datetime import date
from .mascota import Mascota
from .veterinario import Veterinario
from .propietario import Propietario

FECHA_MINIMA_CONSULTA = date(2000, 1, 1)


class Consulta:
    def __init__(
        self, 
        id_consulta: int, 
        motivo: str, 
        fecha_consulta: date, 
        veterinario_id: int, 
        mascota_id: int,
        propietario_id: int
    ):
        self.id_consulta = id_consulta
        self.motivo = motivo
        self.fecha_consulta = fecha_consulta
        self.veterinario_id = veterinario_id
        self.mascota_id = mascota_id
        self.propietario_id = propietario_id

    @property
    def propietario_id(self) -> int:
        return self._propietario_id

    @propietario_id.setter
    def propietario_id(self, nuevo_propietario_id: int):
        if not isinstance(nuevo_propietario_id, int) or isinstance(nuevo_propietario_id, bool):
            raise TypeError("El ID del propietario debe ser un número entero.")
        if nuevo_propietario_id <= 0:
            raise ValueError("El ID del propietario debe ser un número positivo.")
        self._propietario_id = nuevo_propietario_id

    @property
    def id_consulta(self) -> int:
        return self._id_consulta

    @id_consulta.setter
    def id_consulta(self, nuevo_id: int):
        if not isinstance(nuevo_id, int) or isinstance(nuevo_id, bool):
            raise TypeError("El ID de la consulta debe ser un número entero.")
        if nuevo_id <= 0:
            raise ValueError("El ID de la consulta debe ser un número positivo mayor a 0.")
        self._id_consulta = nuevo_id

    @property
    def motivo(self) -> str:
        return self._motivo

    @motivo.setter
    def motivo(self, nuevo_motivo: str):
        if not isinstance(nuevo_motivo, str):
            raise TypeError("El motivo de la consulta debe ser una cadena de texto.")
        if not nuevo_motivo.strip():
            raise ValueError("El motivo de la consulta no puede estar vacío.")
        self._motivo = nuevo_motivo.strip()

    @property
    def fecha_consulta(self) -> date:
        return self._fecha_consulta

    @fecha_consulta.setter
    def fecha_consulta(self, nueva_fecha: date):
        if not isinstance(nueva_fecha, date):
            raise TypeError("La fecha de la consulta debe ser un objeto de tipo date.")
        if nueva_fecha > date.today():
            raise ValueError(f"Fecha inválida. La fecha no puede ser mayor a la fecha actual. Fecha recibida: {nueva_fecha}")
        if nueva_fecha < FECHA_MINIMA_CONSULTA:
            raise ValueError(f"Fecha inválida. La fecha no puede ser menor a {FECHA_MINIMA_CONSULTA.strftime('%d/%m/%Y')}. Fecha recibida: {nueva_fecha}")
        self._fecha_consulta = nueva_fecha


    @property
    def veterinario_id(self) -> int:
        return self._veterinario_id

    @veterinario_id.setter
    def veterinario_id(self, nuevo_vet_id: int):
        if not isinstance(nuevo_vet_id, int) or isinstance(nuevo_vet_id, bool):
            raise TypeError("El ID del veterinario debe ser un número entero.")
        if nuevo_vet_id <= 0:
            raise ValueError("El ID del veterinario debe ser un número positivo.")
        self._veterinario_id = nuevo_vet_id

    @property
    def mascota_id(self) -> int:
        return self._mascota_id

    @mascota_id.setter
    def mascota_id(self, nuevo_mascota_id: int):
        if not isinstance(nuevo_mascota_id, int) or isinstance(nuevo_mascota_id, bool):
            raise TypeError("El ID de la mascota debe ser un número entero.")
        if nuevo_mascota_id <= 0:
            raise ValueError("El ID de la mascota debe ser un número positivo.")
        self._mascota_id = nuevo_mascota_id

    def __repr__(self) -> str:
        return (
            f"Consulta(id={self.id_consulta}, motivo='{self.motivo}', "
            f"fecha={self.fecha_consulta}, vet_id={self.veterinario_id}, "
            f"mascota_id={self.mascota_id})"
        )