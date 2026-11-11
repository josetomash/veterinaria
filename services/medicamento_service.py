import sqlite3

from dao import MedicamentoDAO
from models import Medicamento


class MedicamentoService:
    def __init__(self, medicamento_dao: MedicamentoDAO):
        self._medicamento_dao = medicamento_dao

    def obtener_medicamento_por_id(self, id_medicamento: int) -> Medicamento:
        return self._medicamento_dao.obtener_por_id_estricto(id_medicamento)

    def listar_medicamentos(self) -> list[Medicamento]:
        return self._medicamento_dao.listar_todos()

    def buscar_medicamentos_por_nombre(self, termino: str) -> list[Medicamento]:
        termino_limpio = termino.strip()
        if not termino_limpio:
            raise ValueError("Debe proporcionar un nombre comercial para buscar.")
        return self._medicamento_dao.buscar_por_termino_seguro(termino_limpio)

    def registrar_medicamento(self, medicamento: Medicamento) -> Medicamento:
        if not isinstance(medicamento, Medicamento):
            raise TypeError("Debe proporcionar un medicamento válido.")
        try:
            self._medicamento_dao.insertar(medicamento)
            return medicamento
        except sqlite3.IntegrityError as error:
            nombre_limpio = medicamento.nombre_comercial.strip()
            raise ValueError(f"No se pudo registrar: el medicamento '{nombre_limpio}' ya existe en el sistema.") from error

    def actualizar_medicamento(self, medicamento: Medicamento) -> bool:
        return self._medicamento_dao.actualizar(medicamento)

    def borrar_medicamento(self, id_medicamento: int) -> bool:
        return self._medicamento_dao.eliminar(id_medicamento)

    def poblar_medicamentos_iniciales(self) -> None:
        iniciales = (
            ("Amoxicilina 250 mg", "Amoxicilina", "Antibiótico", 5500, 100),
            ("Meloxicam 1 mg", "Meloxicam", "Antiinflamatorio", 4200, 60),
            ("Carprofeno 25 mg", "Carprofeno", "Antiinflamatorio", 6800, 40),
            ("Enrofloxacino 50 mg", "Enrofloxacino", "Antibiótico", 7300, 50),
            ("Metronidazol 250 mg", "Metronidazol", "Antibiótico", 3900, 45),
        )
        existentes = {medicamento.nombre_comercial for medicamento in self.listar_medicamentos()}
        for nombre, generico, tipo, precio, stock in iniciales:
            if nombre not in existentes:
                self.registrar_medicamento(Medicamento(None, nombre, generico, tipo, precio, stock))
