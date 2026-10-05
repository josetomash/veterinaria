import sqlite3
from models.propietario import Propietario

class PropietarioDAO:  
    def __init__(self, ruta_db: str = "database/clinica_veterinaria.db"):
        self.ruta_db = ruta_db
        self._create_table()

    def _create_table(self):
        pass
    
    def insertar(self, propietario: Propietario) -> None:
        pass