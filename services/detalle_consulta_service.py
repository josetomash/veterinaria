import sqlite3

from dao import DetalleConsultaDAO
from models import DetalleConsulta


class DetalleConsultaService:
    def __init__(self, detalle_consulta_dao: DetalleConsultaDAO):
        self._detalle_consulta_dao = detalle_consulta_dao

    def obtener_detalle_consulta_por_id(self, id_detalle: int) -> DetalleConsulta:
        return self._detalle_consulta_dao.obtener_por_id_estricto(id_detalle)

    def listar_detalles_consulta(self) -> list[DetalleConsulta]:
        return self._detalle_consulta_dao.listar_todos()

    def buscar_detalles_por_consulta(self, id_consulta: int) -> list[DetalleConsulta]:
        return [
            detalle
            for detalle in self._detalle_consulta_dao.listar_todos()
            if detalle.id_consulta == id_consulta
        ]

    def registrar_detalle_consulta(self, detalle: DetalleConsulta) -> DetalleConsulta:
        if not isinstance(detalle, DetalleConsulta):
            raise TypeError("Debe proporcionar un detalle de consulta válido.")
        try:
            self._detalle_consulta_dao.insertar(detalle)
            return detalle
        except sqlite3.IntegrityError as error:
            raise ValueError(f"No se pudo registrar el detalle de consulta: {error}") from error

    def actualizar_detalle_consulta(self, detalle: DetalleConsulta) -> bool:
        return self._detalle_consulta_dao.actualizar(detalle)

    def borrar_detalle_consulta(self, id_detalle: int) -> bool:
        return self._detalle_consulta_dao.eliminar(id_detalle)
