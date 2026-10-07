# veterinaria/main.py
"""
Aplicar inyeccion de dependencias, instanciar conexion a la base de datos
crear la capa de acceso a los datos y inicializar la capa de negocio
y entregar al usuario la interfaz UI
"""

from pathlib import Path

from screens.main_menu import MenuPrincipal
from database.conexion import Conexion
from dao import (
    ConsultaDAO,
    DetalleConsultaDAO,
    EspecialidadDAO,
    EspecieDAO,
    MascotaDAO,
    MedicamentoDAO,
    PropietarioDAO,
    RecetaMedicaDAO,
)
from services import ClinicaService


def main():
    ruta_db = Path(__file__).resolve().parent / "database" / "clinica_veterinaria.db"
    conexion = Conexion(str(ruta_db))
    try:
        clinica_service = ClinicaService(
            medicamento_dao=MedicamentoDAO(conexion),
            consulta_dao=ConsultaDAO(conexion),
            detalle_consulta_dao=DetalleConsultaDAO(conexion),
            especie_dao=EspecieDAO(conexion),
            especialidad_dao=EspecialidadDAO(conexion),
            mascota_dao=MascotaDAO(conexion),
            receta_medica_dao=RecetaMedicaDAO(conexion),
            propietario_dao=PropietarioDAO(conexion),
        )
        menu = MenuPrincipal(clinica_service)
        menu.mostrar_menu()
    finally:
        conexion.cerrar()


if __name__ == "__main__":
    main()