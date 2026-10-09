from datetime import date
import os

from models.especie import Especie
from models.especialidad import Especialidad
from models.mascota import Mascota
from models.propietario import Propietario
from models.veterinario import Veterinario
from services.mascota_service import MascotaService
from services.propietario_service import PropietarioService
from services.veterinario_service import VeterinarioService


class RegistrarMenu:
    def __init__(
        self,
        propietario_service: PropietarioService,
        mascota_service: MascotaService,
        veterinario_service: VeterinarioService,
    ):
        self._propietario_service = propietario_service
        self._mascota_service = mascota_service
        self._veterinario_service = veterinario_service

    def mostrar_menu(self):
        print("=== Menú de Registro ===")
        print("Bienvenido al sistema de gestión veterinaria")
        print("1. Asignar Propietario")
        print("2. Asignar Mascota")
        print("3. Asignar Veterinario")
        print("4. Salir")
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
        return Mascota(id_mascota, nombre, fecha_nacimiento, especies[indice_especie - 1])

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
        id_persona = int(input("ID de persona: "))
        nombre = input("Nombre del veterinario: ").strip()
        rut = input("RUT: ").strip()
        telefono = input("Teléfono (+569...): ").strip()
        id_veterinario = int(input("ID de veterinario: "))
        especialidades = list(Especialidad)
        print("Especialidades:")
        for indice, especialidad in enumerate(especialidades, start=1):
            print(f"{indice}. {especialidad.value}")
        indice_especialidad = int(input("Seleccione una especialidad: "))
        if indice_especialidad < 1 or indice_especialidad > len(especialidades):
            raise ValueError("La especialidad seleccionada no existe.")
        return Veterinario(
            id_persona,
            nombre,
            rut,
            telefono,
            id_veterinario,
            especialidades[indice_especialidad - 1],
        )
