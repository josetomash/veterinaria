from datetime import date
import sqlite3

from models.consulta import Consulta
from models.detalle_consulta import DetalleConsulta
from models.especialidad import Especialidad
from models.especie import Especie
from models.mascota import Mascota
from models.medicamento import Medicamento
from models.propietario import Propietario
from models.receta_medica import RecetaMedica
from models.veterinario import Veterinario
from services.consulta_service import ConsultaService
from services.detalle_consulta_service import DetalleConsultaService
from services.mascota_service import MascotaService
from services.medicamento_service import MedicamentoService
from services.propietario_service import PropietarioService
from services.receta_medica_service import RecetaMedicaService
from services.veterinario_service import VeterinarioService


class ActualizarMenu:
    def __init__(
        self,
        consulta_service: ConsultaService,
        detalle_consulta_service: DetalleConsultaService,
        mascota_service: MascotaService,
        medicamento_service: MedicamentoService,
        propietario_service: PropietarioService,
        receta_medica_service: RecetaMedicaService,
        veterinario_service: VeterinarioService,
    ):
        self._consulta_service = consulta_service
        self._detalle_consulta_service = detalle_consulta_service
        self._mascota_service = mascota_service
        self._medicamento_service = medicamento_service
        self._propietario_service = propietario_service
        self._receta_medica_service = receta_medica_service
        self._veterinario_service = veterinario_service

    def ejecutar(self):
        while True:
            print("\n=== Menú Actualizar ===")
            print("1. Actualizar consulta")
            print("2. Actualizar detalle de consulta")
            print("3. Actualizar mascota")
            print("4. Actualizar medicamento")
            print("5. Actualizar propietario")
            print("6. Actualizar receta médica")
            print("7. Actualizar veterinario")
            print("8. Volver al menú principal")
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self._ejecutar_actualizacion("consulta", self._actualizar_consulta)
            elif opcion == "2":
                self._ejecutar_actualizacion(
                    "detalle de consulta",
                    self._actualizar_detalle_consulta,
                )
            elif opcion == "3":
                self._ejecutar_actualizacion("mascota", self._actualizar_mascota)
            elif opcion == "4":
                self._ejecutar_actualizacion("medicamento", self._actualizar_medicamento)
            elif opcion == "5":
                self._ejecutar_actualizacion("propietario", self._actualizar_propietario)
            elif opcion == "6":
                self._ejecutar_actualizacion(
                    "receta médica",
                    self._actualizar_receta_medica,
                )
            elif opcion == "7":
                self._ejecutar_actualizacion("veterinario", self._actualizar_veterinario)
            elif opcion == "8":
                return
            else:
                print("Opción inválida. Intente nuevamente.")

    def _ejecutar_actualizacion(self, entidad, actualizar):
        try:
            actualizar()
        except (TypeError, ValueError, sqlite3.IntegrityError) as error:
            print(f"No se pudo actualizar {entidad}: {error}")
        else:
            print(f"{entidad.capitalize()} actualizado correctamente.")
        input("Presione Enter para continuar...")

    def _actualizar_consulta(self):
        id_consulta = int(input("ID de la consulta a actualizar: "))
        consulta = Consulta(
            id_consulta,
            input("Motivo: ").strip(),
            date.fromisoformat(input("Fecha (AAAA-MM-DD): ").strip()),
            int(input("ID del veterinario: ")),
            int(input("ID de la mascota: ")),
            int(input("ID del propietario: ")),
        )
        self._consulta_service.actualizar_consulta(consulta)

    def _actualizar_detalle_consulta(self):
        id_detalle = int(input("ID del detalle de consulta a actualizar: "))
        diagnostico = input("Diagnóstico: ").strip()
        tratamiento = input("Tratamiento: ").strip()
        id_receta = int(input("ID de la receta médica asociada: "))
        receta = self._receta_medica_service.obtener_receta_medica_por_id(id_receta)
        detalle = DetalleConsulta(id_detalle, diagnostico, tratamiento, receta)
        self._detalle_consulta_service.actualizar_detalle_consulta(detalle)

    def _actualizar_mascota(self):
        id_mascota = int(input("ID de la mascota a actualizar: "))
        nombre = input("Nombre: ").strip()
        fecha_nacimiento = date.fromisoformat(
            input("Fecha de nacimiento (AAAA-MM-DD): ").strip()
        )
        especies = list(Especie)
        print("Especies:")
        for indice, especie in enumerate(especies, start=1):
            print(f"{indice}. {especie.nombre_especie}")
        indice_especie = int(input("Seleccione una especie: "))
        if indice_especie < 1 or indice_especie > len(especies):
            raise ValueError("La especie seleccionada no existe.")

        mascota = Mascota(
            id_mascota,
            nombre,
            fecha_nacimiento,
            especies[indice_especie - 1],
        )
        self._mascota_service.actualizar_mascota(mascota)

    def _actualizar_medicamento(self):
        medicamento = Medicamento(
            int(input("ID del medicamento a actualizar: ")),
            input("Nombre comercial: ").strip(),
            input("Nombre genérico: ").strip(),
            input("Tipo: ").strip(),
            float(input("Precio: ")),
            int(input("Stock: ")),
        )
        self._medicamento_service.actualizar_medicamento(medicamento)

    def _actualizar_propietario(self):
        id_propietario = int(input("ID del propietario a actualizar: "))
        propietario_actual = self._propietario_service.obtener_propietario_por_id(
            id_propietario
        )
        nombre = input("Nombre: ").strip()
        rut = input("RUT: ").strip()
        telefono = input("Teléfono (+569...): ").strip()
        email = input("Correo electrónico: ").strip()

        mascota = propietario_actual.mascota
        actualizar_mascota = input(
            "¿Desea actualizar también su mascota? (S/N): "
        ).strip().lower()
        if actualizar_mascota == "s":
            mascota = self._crear_mascota(mascota.id_mascota)

        propietario = Propietario(
            nombre,
            rut,
            telefono,
            id_propietario,
            email,
            mascota,
        )
        self._propietario_service.actualizar_propietario(propietario)

    def _crear_mascota(self, id_mascota=None):
        if id_mascota is None:
            id_mascota = int(input("ID de mascota: "))
        nombre = input("Nombre de mascota: ").strip()
        fecha_nacimiento = date.fromisoformat(
            input("Fecha de nacimiento (AAAA-MM-DD): ").strip()
        )
        especies = list(Especie)
        print("Especies:")
        for indice, especie in enumerate(especies, start=1):
            print(f"{indice}. {especie.nombre_especie}")
        indice_especie = int(input("Seleccione una especie: "))
        if indice_especie < 1 or indice_especie > len(especies):
            raise ValueError("La especie seleccionada no existe.")
        return Mascota(
            id_mascota,
            nombre,
            fecha_nacimiento,
            especies[indice_especie - 1],
        )

    def _actualizar_receta_medica(self):
        receta = RecetaMedica(
            int(input("ID de la receta médica a actualizar: ")),
            input("Nombre comercial: ").strip(),
            int(input("Cantidad en mg: ")),
            input("Instrucciones: ").strip(),
        )
        self._receta_medica_service.actualizar_receta_medica(receta)

    def _actualizar_veterinario(self):
        id_veterinario = int(input("ID del veterinario a actualizar: "))
        nombre = input("Nombre: ").strip()
        rut = input("RUT: ").strip()
        telefono = input("Teléfono (+569...): ").strip()
        especialidades = list(Especialidad)
        print("Especialidades:")
        for indice, especialidad in enumerate(especialidades, start=1):
            print(f"{indice}. {especialidad.value}")
        indice_especialidad = int(input("Seleccione una especialidad: "))
        if indice_especialidad < 1 or indice_especialidad > len(especialidades):
            raise ValueError("La especialidad seleccionada no existe.")

        veterinario = Veterinario(
            id_veterinario,
            nombre,
            rut,
            telefono,
            especialidades[indice_especialidad - 1],
        )
        self._veterinario_service.actualizar_veterinario(veterinario)