from dao import (
    ConsultaDAO,
    DetalleConsultaDAO,
    EspecialidadDAO,
    EspecieDAO,
    MascotaDAO,
    MedicamentoDAO,
    RecetaMedicaDAO,
    PropietarioDAO,
)
from models import (
    Consulta,
    DetalleConsulta,
    Especialidad,
    Especie,
    Mascota,
    Medicamento,
    RecetaMedica,
    Propietario,
)
from .consulta_service import ConsultaService
from .detalle_consulta_service import DetalleConsultaService
from .especialidad_service import EspecialidadService
from .especie_service import EspecieService
from .mascota_service import MascotaService
from .medicamento_service import MedicamentoService
from .receta_medica_service import RecetaMedicaService
from .propietario_service import PropietarioService

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
        propietario_dao: PropietarioDAO,
    ):
        self._medicamento_service = MedicamentoService(medicamento_dao)
        self._consulta_service = ConsultaService(consulta_dao)
        self._detalle_consulta_service = DetalleConsultaService(detalle_consulta_dao)
        self._especie_service = EspecieService(especie_dao)
        self._especialidad_service = EspecialidadService(especialidad_dao)
        self._mascota_service = MascotaService(mascota_dao)
        self._receta_medica_service = RecetaMedicaService(receta_medica_dao)
        self._propietario_service = PropietarioService(propietario_dao)
    def registrar_detalle_consulta(self, detalle: DetalleConsulta) -> DetalleConsulta:
        return self._detalle_consulta_service.registrar_detalle_consulta(detalle)

    def registrar_especie(self, especie: Especie) -> Especie:
        return self._especie_service.registrar_especie(especie)

    def registrar_consulta(self, consulta: Consulta) -> Consulta:
        return self._consulta_service.registrar_consulta(consulta)

    def registrar_receta_medica(self, receta: RecetaMedica) -> RecetaMedica:
        return self._receta_medica_service.registrar_receta_medica(receta)

    def registrar_mascota(self, mascota: Mascota) -> Mascota:
        return self._mascota_service.registrar_mascota(mascota)

    def registrar_medicamento(self, medicamento: Medicamento) -> Medicamento:
        return self._medicamento_service.registrar_medicamento(medicamento)

    def registrar_especialidad(self, especialidad: Especialidad) -> Especialidad:
        return self._especialidad_service.registrar_especialidad(especialidad)

    def registrar_propietario(self, propietario: Propietario) -> Propietario:
        return self._propietario_service.registrar_propietario(propietario)