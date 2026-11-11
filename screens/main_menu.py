import sqlite3

from screens.registrar_menu import RegistrarMenu
from screens.menu_consulta import MenuConsulta
from screens.menu_borrar import MenuBorrar
from screens.actualizar_menu import ActualizarMenu
from services.mascota_service import MascotaService
from services.detalle_consulta_service import DetalleConsultaService
from services.medicamento_service import MedicamentoService
from services.propietario_service import PropietarioService
from services.receta_medica_service import RecetaMedicaService
from services.veterinario_service import VeterinarioService
from services.consulta_service import ConsultaService
from services.dolar_service import DolarService
from screens.utilidades import limpiar_pantalla, pausar


class MenuPrincipal:
    def __init__(
        self,
        propietario_service: PropietarioService,
        mascota_service: MascotaService,
        veterinario_service: VeterinarioService,
        menu_consulta: MenuConsulta,
        medicamento_service: MedicamentoService,
        receta_medica_service: RecetaMedicaService,
        detalle_consulta_service: DetalleConsultaService,
        consulta_service: ConsultaService,
        dolar_service: DolarService,
    ):
        self._propietario_service = propietario_service
        self._mascota_service = mascota_service
        self._veterinario_service = veterinario_service
        self._menu_consulta = menu_consulta
        self._medicamento_service = medicamento_service
        self._receta_medica_service = receta_medica_service
        self._detalle_consulta_service = detalle_consulta_service
        self._consulta_service = consulta_service
        self._dolar_service = dolar_service
        self._menu_borrar = MenuBorrar(
            consulta_service,
            propietario_service,
            mascota_service,
            veterinario_service,
            detalle_consulta_service,
            medicamento_service,
            receta_medica_service,
        )
        self._menu_actualizar = ActualizarMenu(
            consulta_service,
            detalle_consulta_service,
            mascota_service,
            medicamento_service,
            propietario_service,
            receta_medica_service,
            veterinario_service,
        )

    def mostrar_menu(self) -> None:
        while True:
            limpiar_pantalla()
            print("\n=== Menú Principal ===")
            print("Bienvenido al sistema de gestión veterinaria")
            print("1. Registrar consulta")
            print("2. Consultar")
            print("3. Borrar")
            print("4. Actualizar")
            print("5. Precios de medicamento")
            print("6. Salir")
            print("======================")
            usuario = input("Seleccione una opción: ").strip()
            try:
                if usuario == "1":
                    registrar_menu = RegistrarMenu(
                        self._propietario_service,
                        self._mascota_service,
                        self._veterinario_service,
                        self._medicamento_service,
                        self._receta_medica_service,
                        self._detalle_consulta_service,
                        self._consulta_service,
                    )
                    registrar_menu.ejecutar()
                elif usuario == "2":
                    self._menu_consulta.ejecutar()
                elif usuario == "3":
                    self._menu_borrar.ejecutar()
                elif usuario == "4":
                    self._menu_actualizar.ejecutar()
                elif usuario == "5":
                    self._mostrar_precios_medicamentos()
                elif usuario == "6":
                    print("Saliendo del sistema...")
                    return
                else:
                    print("Opción no válida. Intente nuevamente.")
                    pausar()
            except sqlite3.OperationalError as error:
                # Por ejemplo: la base de datos esta abierta o bloqueada por otro programa
                print(f"\n[Error de base de datos] {error}")
                print("Cierre otros programas que estén usando la base de datos e intente nuevamente.")
                pausar()

    def _mostrar_precios_medicamentos(self) -> None:
        limpiar_pantalla()
        print("\n=== Precios de medicamento ===")
        dolar = self._dolar_service.obtener_cotizacion()

        # si guardado termino dando None
        if dolar is None:
            print("No fue posible obtener una cotización del dólar.")
            pausar()
            return
        print(f"Cotización: {dolar}")
        for medicamento in self._medicamento_service.listar_medicamentos():
            print(f"{medicamento.nombre_comercial}: ${medicamento.precio:,.0f} CLP")
        pausar()
