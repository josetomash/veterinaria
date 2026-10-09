from database import ConexionDB
from dao import (
    EspecialidadDAO,
    EspecieDAO,
    MascotaDAO,
    PropietarioDAO,
    VeterinarioDAO,
)
from screens.main_menu import MenuPrincipal
from services.mascota_service import MascotaService
from services.propietario_service import PropietarioService
from services.veterinario_service import VeterinarioService


def main():
    conexion_db = ConexionDB()

    EspecieDAO(conexion_db)
    EspecialidadDAO(conexion_db)
    propietario_service = PropietarioService(PropietarioDAO(conexion_db))
    mascota_service = MascotaService(MascotaDAO(conexion_db))
    veterinario_service = VeterinarioService(VeterinarioDAO(conexion_db))

    menu = MenuPrincipal(propietario_service, mascota_service, veterinario_service)
    menu.mostrar_menu()


if __name__ == "__main__":
    main()
