# veterinaria/main.py
"""
Aplicar inyeccion de dependencias, instanciar conexion a la base de datos
crear la capa de acceso a los datos y inicializar la capa de negocio
y entregar al usuario la interfaz UI
"""

from screens.main_menu import MenuPrincipal
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
    clinica_service = ClinicaService(
        medicamento_dao=MedicamentoDAO(),
        consulta_dao=ConsultaDAO(),
        detalle_consulta_dao=DetalleConsultaDAO(),
        especie_dao=EspecieDAO(),
        especialidad_dao=EspecialidadDAO(),
        mascota_dao=MascotaDAO(),
        receta_medica_dao=RecetaMedicaDAO(),
        propietario_dao=PropietarioDAO(),
    )
    menu = MenuPrincipal(clinica_service)
    menu.mostrar_menu()


if __name__ == "__main__":
    main()