import sqlite3

from database import ConexionDB
from dao import (
    ConsultaDAO,
    DetalleConsultaDAO,
    EspecialidadDAO,
    EspecieDAO,
    MascotaDAO,
    MedicamentoDAO,
    PropietarioDAO,
    RecetaMedicaDAO,
    VeterinarioDAO,
)
from screens.menu_consulta import MenuConsulta
from screens.main_menu import MenuPrincipal
from services.consulta_service import ConsultaService
from services.detalle_consulta_service import DetalleConsultaService
from services.especie_service import EspecieService
from services.mascota_service import MascotaService
from services.medicamento_service import MedicamentoService
from services.propietario_service import PropietarioService
from services.receta_medica_service import RecetaMedicaService
from services.veterinario_service import VeterinarioService


def main():
    conexion_db = ConexionDB()
    print(f"Base de datos: {conexion_db.ruta_db}")

    # se inicializan los servicios con los respectivos DAOs 
    especie_service = EspecieService(EspecieDAO(conexion_db))
    EspecialidadDAO(conexion_db)
    propietario_service = PropietarioService(PropietarioDAO(conexion_db))
    mascota_service = MascotaService(MascotaDAO(conexion_db))
    veterinario_service = VeterinarioService(VeterinarioDAO(conexion_db))
    consulta_service = ConsultaService(ConsultaDAO(conexion_db))
    receta_medica_service = RecetaMedicaService(RecetaMedicaDAO(conexion_db))
    detalle_consulta_service = DetalleConsultaService(DetalleConsultaDAO(conexion_db))
    medicamento_service = MedicamentoService(MedicamentoDAO(conexion_db))

    # construye el menu y
    # se le entrega el servicio que necesita
    menu_consulta = MenuConsulta(
        mascota_service,
        propietario_service,
        veterinario_service,
        consulta_service,
        especie_service,
        detalle_consulta_service,
        receta_medica_service,
        medicamento_service,
    )
    menu = MenuPrincipal(
        propietario_service,
        mascota_service,
        veterinario_service,
        menu_consulta,
        medicamento_service,
        receta_medica_service,
        detalle_consulta_service,
        consulta_service,
    )
    menu.mostrar_menu()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C o cierre de la entrada: se sale sin mostrar el error de Python
        print("\nSaliendo del sistema...")
    except sqlite3.Error as error:
        print(f"\n[Error de base de datos] {error}")
        print(
            "Revise la ruta de la base de datos, los permisos de escritura "
            "y que el archivo no esté bloqueado por otro programa."
        )
