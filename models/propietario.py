import re
from .persona import Persona

class Propietario(Persona):
  
  def __init__(self, rut: str, nombre_completo: str, id_propietario: int, email: str, nombre_email: str, telefono: str):
    super().__init__(rut, nombre_completo)
    self.__id_propietario = id_propietario
    self.__email = email
    self.__nombre_email = nombre_email
    self.actualizar_telefono = telefono  

  @property
  def actualizar_telefono(self):
    return self.__telefono

  @actualizar_telefono.setter
  def actualizar_telefono(self, nuevo_telefono):
    if nuevo_telefono == self.__telefono:
      raise ValueError(
        "El nuevo telefono no debe ser igual al actual"
      )
    # borrar espacios, parentesis, guiones. El \ es para indicar al re que son 
    numero_limpio = re.sub(r'[\s\-\(\)]', '', nuevo_telefono)
    patron = r'^\+?\d{7,15}$'
    
    if not re.match(patron, numero_limpio):
      raise ValueError("El formato del teléfono no es válido (debe tener entre 7 y 15 dígitos).")
    
    self.__telefono = numero_limpio

class PropietarioBuilder:
  def __init__(self):
    self._rut = None
    self._nombre_completo = None
    self._id_propietario = None
    self._email = None
    self._nombre_email = None
    self._telefono = None

  def set_rut(self, rut: str):
    self._rut = rut
    return self

  def set_nombre_completo(self, nombre: str):
    self._nombre_completo = nombre
    return self

  def set_id_propietario(self, id_propietario: int):
    self._id_propietario = id_propietario
    return self

  def set_email(self, email: str):
    self._email = email
    return self

  def set_nombre_email(self, nombre_email: str):
    self._nombre_email = nombre_email
    return self

  def set_telefono(self, telefono: str):
    self._telefono = telefono
    return self

  def build(self) -> Propietario:
    if not self._rut or not self._nombre_completo:
      raise ValueError(
        "Debe implementar de manera obligatoria" \
        "\nel rut y el nombre completo de propietario"
        )

    return Propietario(
        rut=self._rut,
        nombre_completo=self._nombre_completo,
        id_propietario=self._id_propietario,
        email=self._email,
        nombre_email=self._nombre_email,
        telefono=self._telefono,
    )