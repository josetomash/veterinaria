import sqlite3

from dao import ConsultaDAO
from models import Consulta


class ConsultaService:
    def __init__(self, consulta_dao: ConsultaDAO):
        self._consulta_dao = consulta_dao

    def obtener_consulta_por_id(self, id_consulta: int) -> Consulta:
        return self._consulta_dao.obtener_por_id_estricto(id_consulta)

    def listar_consultas(self) -> list[Consulta]:
        return self._consulta_dao.listar_todos()

    def buscar_consultas_por_propietario(self, id_propietario: int) -> list[Consulta]:
        consultas = [
            consulta
            for consulta in self._consulta_dao.listar_todos()
            if consulta.propietario_id == id_propietario
        ]
        # De la más antigua a la más nueva
        return sorted(consultas, key=lambda consulta: (consulta.fecha_consulta, consulta.id_consulta))

    def registrar_consulta(self, consulta: Consulta) -> Consulta:
        if not isinstance(consulta, Consulta):
            raise TypeError("Debe proporcionar una consulta válida.")
        try:
            self._consulta_dao.insertar(consulta)
            return consulta
        except sqlite3.IntegrityError as error:
            raise ValueError(f"No se pudo registrar la consulta: {error}") from error

    def actualizar_consulta(self, consulta: Consulta) -> bool:
        return self._consulta_dao.actualizar(consulta)

    def borrar_consulta(self, id_consulta: int) -> bool:
        return self._consulta_dao.eliminar(id_consulta)
