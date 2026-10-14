from datetime import date
import os

from models.especie import Especie
from models.especialidad import Especialidad
from models.consulta import Consulta
from models.detalle_consulta import DetalleConsulta
from models.mascota import Mascota
from models.medicamento import Medicamento
from models.propietario import Propietario
from models.receta_medica import RecetaMedica
from models.veterinario import Veterinario
from services.detalle_consulta_service import DetalleConsultaService
from services.consulta_service import ConsultaService
from services.mascota_service import MascotaService
from services.medicamento_service import MedicamentoService
from services.propietario_service import PropietarioService
from services.receta_medica_service import RecetaMedicaService
from services.veterinario_service import VeterinarioService


class RegistrarMenu:
    def __init__(
        self,
        propietario_service: PropietarioService,
        mascota_service: MascotaService,
        veterinario_service: VeterinarioService,
        medicamento_service: MedicamentoService,
        receta_medica_service: RecetaMedicaService,
        detalle_consulta_service: DetalleConsultaService,
        consulta_service: ConsultaService,
    ):
        self._propietario_service = propietario_service
        self._mascota_service = mascota_service
        self._veterinario_service = veterinario_service
        self._medicamento_service = medicamento_service
        self._receta_medica_service = receta_medica_service
        self._detalle_consulta_service = detalle_consulta_service
        self._consulta_service = consulta_service

    def mostrar_menu(self):
        print("=== Menú de Registro ===")
        print("Bienvenido al sistema de gestión veterinaria")
        print("1. Asignar Propietario")
        print("2. Asignar Mascota")
        print("3. Asignar Veterinario")
        print("4. Registrar Medicamento")
        print("5. Registrar Receta Médica")
        print("6. Registrar Detalle de Consulta")
        print("7. Registrar Consulta")
        print("8. Salir")
        print("======================")
        return input("Seleccione una opción: ").strip()

    def ejecutar(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            opcion = self.mostrar_menu()
            if opcion == "1":
                respuesta = input("¿Desea registrar un propietario? (S/N): ").strip()
                if respuesta.lower() == "s":
                    self._registrar_propietario()
            elif opcion == "2":
                self._registrar_mascota()
            elif opcion == "3":
                self._registrar_veterinario()
            elif opcion == "4":
                self._registrar_medicamento()
            elif opcion == "5":
                self._registrar_receta_medica()
            elif opcion == "6":
                self._registrar_detalle_consulta()
            elif opcion == "7":
                self._registrar_consulta()
            elif opcion == "8":
                print("Saliendo del menú de registro...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")

    def _registrar_propietario(self):
        try:
            propietario = self._crear_propietario()
            self._propietario_service.registrar_propietario(propietario)
            print("[OK] Registro de propietario exitoso.")
            input("Presione Enter para continuar...")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
            input("Presione Enter para reintentar...")

    def _registrar_mascota(self):
        try:
            mascota = self._crear_mascota()
            self._mascota_service.registrar_mascota(mascota)
            print("[OK] Registro de mascota exitoso.")
            input("Presione Enter para continuar...")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
            input("Presione Enter para reintentar...")

    def _registrar_veterinario(self):
        try:
            veterinario = self._crear_veterinario()
            self._veterinario_service.registrar_veterinario(veterinario)
            print("[OK] Registro de veterinario exitoso.")
            input("Presione Enter para continuar...")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
            input("Presione Enter para reintentar...")

    def _registrar_medicamento(self):
        try:
            medicamento = self._crear_medicamento()
            self._medicamento_service.registrar_medicamento(medicamento)
            print("[OK] Registro de medicamento exitoso.")
            input("Presione Enter para continuar...")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
            input("Presione Enter para reintentar...")

    def _registrar_receta_medica(self):
        try:
            receta = self._crear_receta_medica()
            self._receta_medica_service.registrar_receta_medica(receta)
            print("[OK] Registro de receta médica exitoso.")
            input("Presione Enter para continuar...")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
            input("Presione Enter para reintentar...")

    def _registrar_detalle_consulta(self):
        try:
            detalle = self._crear_detalle_consulta()
            self._detalle_consulta_service.registrar_detalle_consulta(detalle)
            print("[OK] Registro de detalle de consulta exitoso.")
            input("Presione Enter para continuar...")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
            input("Presione Enter para reintentar...")

    def _registrar_consulta(self):
        try:
            consulta = self._crear_consulta()
            self._consulta_service.registrar_consulta(consulta)
            print("[OK] Registro de consulta exitoso.")
            input("Presione Enter para continuar...")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
            input("Presione Enter para reintentar...")

    def _crear_consulta(self) -> Consulta:
        return Consulta(
            int(input("ID de consulta: ")),
            input("Motivo: ").strip(),
            date.fromisoformat(input("Fecha (AAAA-MM-DD): ").strip()),
            int(input("ID del veterinario: ")),
            int(input("ID de la mascota: ")),
            int(input("ID del propietario: ")),
        )

    def _crear_mascota(self) -> Mascota:
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

    def _crear_propietario(self) -> Propietario:
        mascota = self._crear_mascota()
        return Propietario(
            nombre=input("Nombre del propietario: ").strip(),
            rut=input("RUT: ").strip(),
            telefono=input("Teléfono (+569...): ").strip(),
            id_propietario=int(input("ID de propietario: ")),
            email=input("Correo electrónico: ").strip(),
            mascota=mascota,
        )

    def _crear_veterinario(self) -> Veterinario:
        id_veterinario = int(input("ID de veterinario: "))
        nombre = input("Nombre del veterinario: ").strip()
        rut = input("RUT: ").strip()
        telefono = input("Teléfono (+569...): ").strip()
        especialidades = list(Especialidad)
        print("Especialidades:")
        for indice, especialidad in enumerate(especialidades, start=1):
            print(f"{indice}. {especialidad.value}")
        indice_especialidad = int(input("Seleccione una especialidad: "))
        if indice_especialidad < 1 or indice_especialidad > len(especialidades):
            raise ValueError("La especialidad seleccionada no existe.")
        return Veterinario(
            id_veterinario,
            nombre,
            rut,
            telefono,
            especialidades[indice_especialidad - 1],
        )

    def _crear_medicamento(self) -> Medicamento:
        return Medicamento(
            int(input("ID de medicamento: ")),
            input("Nombre comercial: ").strip(),
            input("Nombre genérico: ").strip(),
            input("Tipo de medicamento: ").strip(),
            float(input("Precio: ")),
            int(input("Stock: ")),
        )

    def _crear_receta_medica(self) -> RecetaMedica:
        id_veterinario = int(input("ID del veterinario que prescribe: "))
        veterinario = self._veterinario_service.obtener_veterinario_por_id(id_veterinario)
        return RecetaMedica(
            int(input("ID de receta: ")),
            input("Nombre comercial del medicamento: ").strip(),
            int(input("Cantidad en mg: ")),
            input("Instrucciones: ").strip(),
            veterinario,
        )

    def _crear_detalle_consulta(self) -> DetalleConsulta:
        id_consulta = int(input("ID de la consulta asociada: "))
        consulta = self._consulta_service.obtener_consulta_por_id(id_consulta)
        id_receta = int(input("ID de la receta médica: "))
        receta = self._receta_medica_service.obtener_receta_medica_por_id(id_receta)
        return DetalleConsulta(
            int(input("ID del detalle de consulta: ")),
            input("Diagnóstico: ").strip(),
            input("Tratamiento: ").strip(),
            receta,
            consulta,
        )
