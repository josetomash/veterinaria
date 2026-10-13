from collections.abc import Iterable

from models import Especie
from services.consulta_service import ConsultaService
from services.detalle_consulta_service import DetalleConsultaService
from services.especie_service import EspecieService
from services.mascota_service import MascotaService
from services.medicamento_service import MedicamentoService
from services.propietario_service import PropietarioService
from services.receta_medica_service import RecetaMedicaService
from services.veterinario_service import VeterinarioService


class MenuConsulta:
    def __init__(
        self,
        mascota_service: MascotaService,
        propietario_service: PropietarioService,
        veterinario_service: VeterinarioService,
        consulta_service: ConsultaService,
        especie_service: EspecieService,
        detalle_consulta_service: DetalleConsultaService,
        receta_medica_service: RecetaMedicaService,
        medicamento_service: MedicamentoService,
    ):
        self._mascota_service = mascota_service
        self._propietario_service = propietario_service
        self._veterinario_service = veterinario_service
        self._consulta_service = consulta_service
        self._especie_service = especie_service
        self._detalle_consulta_service = detalle_consulta_service
        self._receta_medica_service = receta_medica_service
        self._medicamento_service = medicamento_service

    def consultar_menu(self) -> str:
        print("\n=== Menú de Consulta ===")
        print("1. Consultar consulta por ID")
        print("2. Consultar detalle de consulta por ID")
        print("3. Consultar receta médica por ID")
        print("4. Consultar medicamento por ID")
        print("5. Consultar mascota por ID")
        print("6. Consultar propietario por ID")
        print("7. Consultar veterinario por ID")
        print("8. Consultar especie por ID")
        print("9. Consultar mascota por nombre")
        print("10. Consultar mascota por especie")
        print("11. Consultar mascota por edad")
        print("12. Consultar por dueño")
        print("13. Listar registros")
        print("14. Volver al Menú Principal")
        print("========================")
        return input("Seleccione una opción: ").strip()

    def ejecutar(self) -> None:
        while True:
            respuesta = self.consultar_menu()
            if respuesta == "14":
                return
            try:
                if respuesta == "1":
                    self._consultar_por_id(
                        "consulta",
                        self._consulta_service.obtener_consulta_por_id,
                    )
                elif respuesta == "2":
                    self._consultar_por_id(
                        "detalle de consulta",
                        self._detalle_consulta_service.obtener_detalle_consulta_por_id,
                    )
                elif respuesta == "3":
                    self._consultar_por_id(
                        "receta médica",
                        self._receta_medica_service.obtener_receta_medica_por_id,
                    )
                elif respuesta == "4":
                    self._consultar_por_id(
                        "medicamento",
                        self._medicamento_service.obtener_medicamento_por_id,
                    )
                elif respuesta == "5":
                    self._consultar_por_id(
                        "mascota",
                        self._mascota_service.obtener_mascota_por_id,
                    )
                elif respuesta == "6":
                    self._consultar_por_id(
                        "propietario",
                        self._propietario_service.obtener_propietario_por_id,
                    )
                elif respuesta == "7":
                    self._consultar_por_id(
                        "veterinario",
                        self._veterinario_service.obtener_veterinario_por_id,
                    )
                elif respuesta == "8":
                    self._consultar_por_id(
                        "especie",
                        self._especie_service.obtener_especie_por_id,
                    )
                elif respuesta == "9":
                    self._consultar_mascotas_por_nombre()
                elif respuesta == "10":
                    self._consultar_mascotas_por_especie()
                elif respuesta == "11":
                    self._consultar_mascotas_por_edad()
                elif respuesta == "12":
                    self._consultar_propietarios_por_nombre()
                elif respuesta == "13":
                    self._listar_registros()
                else:
                    print("Opción no válida. Intente nuevamente.")
                    continue
            except (ValueError, TypeError) as error:
                print(f"\n[Error de consulta] {error}")
            input("Presione Enter para continuar...")

    def _listar_registros(self) -> None:
        print("\n=== Listar registros ===")
        print("1. Mascotas")
        print("2. Propietarios")
        print("3. Veterinarios")
        print("4. Consultas")
        print("5. Especies")
        print("6. Detalles de consulta")
        print("7. Recetas médicas")
        print("8. Medicamentos")
        print("9. Volver")
        opcion = input("Seleccione qué desea listar: ").strip()

        if opcion == "1":
            resultados = self._mascota_service.listar_mascotas()
        elif opcion == "2":
            resultados = self._propietario_service.listar_propietarios()
        elif opcion == "3":
            resultados = self._veterinario_service.listar_veterinarios()
        elif opcion == "4":
            resultados = self._consulta_service.listar_consultas()
        elif opcion == "5":
            resultados = self._especie_service.listar_especies()
        elif opcion == "6":
            resultados = self._detalle_consulta_service.listar_detalles_consulta()
        elif opcion == "7":
            resultados = self._receta_medica_service.listar_recetas_medicas()
        elif opcion == "8":
            resultados = self._medicamento_service.listar_medicamentos()
        elif opcion == "9":
            return
        else:
            print("Opción no válida. Intente nuevamente.")
            return

        self._imprimir_resultados(resultados)

    def _consultar_por_id(self, entidad, obtener_por_id) -> None:
        id_entidad = int(input("Ingrese el ID: "))
        resultado = obtener_por_id(id_entidad)
        print(f"\n=== Resultado: {entidad} ===")
        self._imprimir_resultado(resultado)

    def _consultar_mascotas_por_nombre(self) -> None:
        termino = input("Ingrese el nombre (o parte del nombre) de la mascota: ")
        resultados = self._mascota_service.buscar_mascotas_por_nombre(termino)
        self._imprimir_resultados(resultados)

    def _consultar_mascotas_por_especie(self) -> None:
        termino = input("Ingrese la especie (o parte del nombre): ")
        resultados = self._mascota_service.buscar_mascotas_por_especie(termino)
        self._imprimir_resultados(resultados)

    def _consultar_mascotas_por_edad(self) -> None:
        edad = int(input("Ingrese la edad de la mascota en años: "))
        resultados = self._mascota_service.buscar_mascotas_por_edad(edad)
        self._imprimir_resultados(resultados)

    def _consultar_propietarios_por_nombre(self) -> None:
        termino = input("Ingrese el nombre (o parte del nombre) del dueño: ")
        resultados = self._propietario_service.buscar_propietarios_por_nombre(termino)
        self._imprimir_resultados(resultados)

    @staticmethod
    def _imprimir_resultados(resultados: Iterable[object]) -> None:
        resultados = list(resultados)
        if not resultados:
            print("No se encontraron resultados.")
            return
        for resultado in resultados:
            MenuConsulta._imprimir_resultado(resultado)

    @staticmethod
    def _imprimir_resultado(resultado: object) -> None:
        if isinstance(resultado, Especie):
            print(
                f"ID Especie: {resultado.id_especie}\n"
                f"Nombre: {resultado.nombre_especie}\n"
                f"Información: {resultado.informacion_especie}"
            )
        else:
            print(resultado)
