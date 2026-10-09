import sqlite3

from dao import MedicamentoDAO
from models import Medicamento


class MedicamentoService:
    def __init__(self, medicamento_dao: MedicamentoDAO):
        self._medicamento_dao = medicamento_dao

    def registrar_medicamento(self, medicamento: Medicamento) -> Medicamento:
        if not isinstance(medicamento, Medicamento):
            raise TypeError("Debe proporcionar un medicamento válido.")
        try:
            self._medicamento_dao.insertar(medicamento)
            return medicamento
        except sqlite3.IntegrityError as error:
            nombre_limpio = medicamento.nombre_comercial.strip()
            raise ValueError(f"No se pudo registrar: el medicamento '{nombre_limpio}' ya existe en el sistema.") from error
