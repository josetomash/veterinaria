from screens.registrar_menu import RegistrarMenu
from screens.menu_consulta import MenuConsulta
from services.mascota_service import MascotaService
from services.propietario_service import PropietarioService
from services.veterinario_service import VeterinarioService


class MenuPrincipal:
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
        print("=== Menú Principal ===")
        print("Bienvenido al sistema de gestión veterinaria")
        print("1. Registrar consulta")
        print("2. Consultar consulta")
        print("3. Salir")
        print("======================")
        usuario = input("Seleccione una opción: ")
        if usuario == "1":
            registrar_menu = RegistrarMenu(
                self._propietario_service,
                self._mascota_service,
                self._veterinario_service,
            )
            registrar_menu.ejecutar()
        elif usuario == "2":
            return "2"
        elif usuario == "3":
            return "3"
