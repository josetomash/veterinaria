from enum import Enum

class Especie(Enum):
    CANINO = (1, "Canino", "Animal doméstico, familia Canidae")
    FELINO = (2, "Felino", "Animal doméstico, familia Felidae")

    def __init__(self, id_especie: int, nombre_especie: str, informacion_especie: str):
        self.id_especie = id_especie
        self.nombre_especie = nombre_especie
        self.informacion_especie = informacion_especie