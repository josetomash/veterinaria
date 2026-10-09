from enum import Enum

class Especie(Enum):
    CANINO = (1, "Canino", "Animal doméstico, familia Canidae")
    FELINO = (2, "Felino", "Animal doméstico, familia Felidae")

    def __init__(self, id_especie: int, nombre_especie: str, informacion_especie: str):
        self._id_especie = id_especie
        self._nombre_especie = nombre_especie
        self._informacion_especie = informacion_especie

    @property
    def id_especie(self) -> int:
        return self._id_especie

    @property
    def nombre_especie(self) -> str:
        return self._nombre_especie

    @property
    def informacion_especie(self) -> str:
        return self._informacion_especie