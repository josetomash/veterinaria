import sqlite3

from dao import (
    MedicamentoDAO,
    ConsultaDAO,
    EspecialidadDAO,
    DetalleConsultaDAO,
    EspecieDAO,
    RecetaMedicaDAO,
    MascotaDAO,
)
from models import (
    Medicamento,
    Consulta,
    DetalleConsulta,
    Especie,
    Especialidad,
    Mascota,
    RecetaMedica,
)


class ClinicaService:
    def __init__(
        self,
        medicamento_dao: MedicamentoDAO,
        consulta_dao: ConsultaDAO,
        detalle_consulta_dao: DetalleConsultaDAO,
        especie_dao: EspecieDAO,
        especialidad_dao: EspecialidadDAO,
        mascota_dao: MascotaDAO,
        receta_medica_dao: RecetaMedicaDAO,
    ):
        self._medicamento_dao = medicamento_dao
        self._consulta_dao = consulta_dao
        self._detalle_consulta_dao = detalle_consulta_dao
        self._especie_dao = especie_dao
        self._especialidad_dao = especialidad_dao
        self._mascota_dao = mascota_dao
        self._receta_medica_dao = receta_medica_dao

    def registrar_detalle_consulta(self, detalle: DetalleConsulta) -> DetalleConsulta:
        if not isinstance(detalle, DetalleConsulta):
            raise TypeError("Debe proporcionar un detalle de consulta válido.")
        try:
            self._detalle_consulta_dao.insertar(detalle)
            return detalle
        except sqlite3.IntegrityError as error:
            raise ValueError(f"No se pudo registrar el detalle de consulta: {error}") from error

    def registrar_especie(self, especie: Especie) -> Especie:
        if not isinstance(especie, Especie):
            raise TypeError("Debe proporcionar una especie válida.")
        try:
            self._especie_dao.insertar(especie)
            return especie
        except sqlite3.IntegrityError as error:
            nombre_limpio = especie.nombre.strip()
            raise ValueError(f"No se pudo registrar: la especie '{nombre_limpio}' ya existe en el sistema.") from error

    def registrar_consulta(self, consulta: Consulta) -> Consulta:
        if not isinstance(consulta, Consulta):
            raise TypeError("Debe proporcionar una consulta válida.")
        try:
            self._consulta_dao.insertar(consulta)
            return consulta
        except sqlite3.IntegrityError as error:
            raise ValueError(f"No se pudo registrar la consulta: {error}") from error

    def registrar_receta_medica(self, receta: RecetaMedica) -> RecetaMedica:
        if not isinstance(receta, RecetaMedica):
            raise TypeError("Debe proporcionar una receta médica válida.")
        try:
            self._receta_medica_dao.insertar(receta)
            return receta
        except sqlite3.IntegrityError as error:
            nombre_limpio = receta.nombre_comercial.strip()
            raise ValueError(f"No se pudo registrar: la receta médica '{nombre_limpio}' ya existe en el sistema.") from error

    def registrar_mascota(self, mascota: Mascota) -> Mascota:
        if not isinstance(mascota, Mascota):
            raise TypeError("Debe proporcionar una mascota válida.")
        try:
            self._mascota_dao.insertar(mascota)
            return mascota
        except sqlite3.IntegrityError as error:
            nombre_limpio = mascota.nombre.strip()
            raise ValueError(f"No se pudo registrar: la mascota '{nombre_limpio}' ya existe en el sistema.") from error

    def registrar_medicamento(self, medicamento: Medicamento) -> Medicamento:
        if not isinstance(medicamento, Medicamento):
            raise TypeError("Debe proporcionar un medicamento válido.")
        try:
            self._medicamento_dao.insertar(medicamento)
            return medicamento
        except sqlite3.IntegrityError as error:
            nombre_limpio = medicamento.nombre.strip()
            raise ValueError(f"No se pudo registrar: el medicamento '{nombre_limpio}' ya existe en el sistema.") from error

    def registrar_especialidad(self, especialidad: Especialidad) -> Especialidad:
        if not isinstance(especialidad, Especialidad):
            raise TypeError("Debe proporcionar una especialidad válida del Enum Especialidad.")
        try:
            self._especialidad_dao.insertar(especialidad)
            return especialidad
        except sqlite3.IntegrityError as error:
            nombre_limpio = especialidad.value.strip()
            raise ValueError(f"No se pudo registrar: la especialidad '{nombre_limpio}' ya existe en el sistema.") from error