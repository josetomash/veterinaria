from screens.registrar_menu import RegistrarMenu
from services.clinica_service import ClinicaService


class MenuPrincipal:
    def __init__(self, clinica_service: ClinicaService):
        self._clinica_service = clinica_service

    def mostrar_menu(self):
        print("=== Menú Principal ===")
        print("Bienvenido al sistema de gestión veterinaria")
        print("1. Registrar consulta")
        print("2. Consultar consulta")
        print("3. Salir")
        print("======================")
        usuario = input("Seleccione una opción: ")
        if usuario == "1":
            registrar_menu = RegistrarMenu(self._clinica_service)
            registrar_menu.ejecutar()
        elif usuario == "2":
            return "2"
        elif usuario == "3":
            return "3"
