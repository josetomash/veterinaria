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
from screens.utilidades import convertir_entero, limpiar_pantalla, pausar, pedir_dato


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
        limpiar_pantalla()
        print("\n=== Menú de Consulta ===")
        print("1. Consultar consultas por RUT del propietario")
        print("2. Consultar recetas médicas por RUT del propietario")
        print("3. Consultar medicamento por nombre comercial")
        print("4. Consultar mascotas por RUT del propietario")
        print("5. Buscar mascotas por nombre")
        print("6. Consultar propietario por RUT")
        print("7. Consultar veterinario por RUT")
        print("8. Consultar especie por nombre")
        print("9. Consultar mascota por especie")
        print("10. Consultar mascota por edad")
        print("11. Consultar por dueño")
        print("12. Listar registros")
        print("13. Volver al Menú Principal")
        print("========================")
        return input("Seleccione una opción: ").strip()

    def ejecutar(self) -> None:
        while True:
            respuesta = self.consultar_menu()
            if respuesta == "13":
                return
            try:
                if respuesta == "1":
                    self._consultar_consultas_por_rut()
                elif respuesta == "2":
                    self._consultar_recetas_por_rut()
                elif respuesta == "3":
                    self._consultar_medicamentos_por_nombre()
                elif respuesta == "4":
                    self._consultar_mascotas_por_rut()
                elif respuesta == "5":
                    self._consultar_mascotas_por_nombre()
                elif respuesta == "6":
                    self._consultar_por_rut(
                        "propietario",
                        self._propietario_service.obtener_propietario_por_rut,
                    )
                elif respuesta == "7":
                    self._consultar_por_rut(
                        "veterinario",
                        self._veterinario_service.obtener_veterinario_por_rut,
                    )
                elif respuesta == "8":
                    self._consultar_especies_por_nombre()
                elif respuesta == "9":
                    self._consultar_mascotas_por_especie()
                elif respuesta == "10":
                    self._consultar_mascotas_por_edad()
                elif respuesta == "11":
                    self._consultar_propietarios_por_nombre()
                elif respuesta == "12":
                    if self._listar_registros() is False:
                        continue  # eligió "Volver": no hace falta pausar
                else:
                    print("Opción no válida. Intente nuevamente.")
            except (ValueError, TypeError) as error:
                print(f"\n[Error de consulta] {error}")
            pausar()

    def _listar_registros(self) -> None:
        limpiar_pantalla()
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
            return False
        else:
            print("Opción no válida. Intente nuevamente.")
            return

        self._imprimir_resultados(resultados)

    def _consultar_por_rut(self, entidad, obtener_por_rut) -> None:
        resultado = pedir_dato(f"Ingrese el RUT del {entidad}: ", obtener_por_rut)
        print(f"\n=== Resultado: {entidad} ===")
        self._imprimir_resultado(resultado)

    def _consultar_consultas_por_rut(self) -> None:
        propietario = pedir_dato(
            "Ingrese el RUT del propietario: ",
            self._propietario_service.obtener_propietario_por_rut,
        )
        consultas = self._consulta_service.buscar_consultas_por_propietario(
            propietario.id_propietario
        )
        if not consultas:
            print("El propietario no tiene consultas registradas.")
            return
        print(f"\n=== Consultas de {propietario.nombre} (de la más antigua a la más nueva) ===")
        for consulta in consultas:
            print("-" * 40)
            print(
                f"Consulta #{consulta.id_consulta} | "
                f"Fecha: {consulta.fecha_consulta.strftime('%d/%m/%Y')}\n"
                f"Motivo: {consulta.motivo}\n"
                f"ID Mascota: {consulta.mascota_id} | "
                f"ID Veterinario: {consulta.veterinario_id}"
            )
            # El detalle de la consulta se muestra junto con ella
            detalles = self._detalle_consulta_service.buscar_detalles_por_consulta(
                consulta.id_consulta
            )
            if not detalles:
                print("Detalle: (sin detalle registrado)")
            for detalle in detalles:
                print("--- Detalle de la consulta ---")
                print(detalle)

    def _consultar_recetas_por_rut(self) -> None:
        propietario = pedir_dato(
            "Ingrese el RUT del propietario: ",
            self._propietario_service.obtener_propietario_por_rut,
        )
        consultas = self._consulta_service.buscar_consultas_por_propietario(
            propietario.id_propietario
        )
        hay_recetas = False
        print(f"\n=== Recetas médicas de {propietario.nombre} (de la más antigua a la más nueva) ===")
        for consulta in consultas:
            detalles = self._detalle_consulta_service.buscar_detalles_por_consulta(
                consulta.id_consulta
            )
            for detalle in detalles:
                hay_recetas = True
                print("-" * 40)
                print(
                    f"Consulta #{consulta.id_consulta} del "
                    f"{consulta.fecha_consulta.strftime('%d/%m/%Y')}"
                )
                print(detalle.receta)
        if not hay_recetas:
            print("El propietario no tiene recetas médicas registradas.")

    def _consultar_medicamentos_por_nombre(self) -> None:
        resultados = pedir_dato(
            "Ingrese el nombre comercial (o parte del nombre) del medicamento: ",
            self._medicamento_service.buscar_medicamentos_por_nombre,
        )
        self._imprimir_resultados(resultados)

    def _consultar_mascotas_por_rut(self) -> None:
        resultados = pedir_dato(
            "Ingrese el RUT del dueño: ",
            self._propietario_service.buscar_mascotas_por_rut,
        )
        self._imprimir_resultados(resultados)

    def _consultar_especies_por_nombre(self) -> None:
        resultados = pedir_dato(
            "Ingrese el nombre (o parte del nombre) de la especie: ",
            self._especie_service.buscar_especies_por_nombre,
        )
        self._imprimir_resultados(resultados)

    def _consultar_mascotas_por_nombre(self) -> None:
        resultados = pedir_dato(
            "Ingrese el nombre (o parte del nombre) de la mascota: ",
            self._mascota_service.buscar_mascotas_por_nombre,
        )
        self._imprimir_resultados(resultados)

    def _consultar_mascotas_por_especie(self) -> None:
        resultados = pedir_dato(
            "Ingrese la especie (o parte del nombre): ",
            self._mascota_service.buscar_mascotas_por_especie,
        )
        self._imprimir_resultados(resultados)

    def _consultar_mascotas_por_edad(self) -> None:
        resultados = pedir_dato(
            "Ingrese la edad de la mascota en años: ",
            lambda texto: self._mascota_service.buscar_mascotas_por_edad(convertir_entero(texto)),
        )
        self._imprimir_resultados(resultados)

    def _consultar_propietarios_por_nombre(self) -> None:
        resultados = pedir_dato(
            "Ingrese el nombre (o parte del nombre) del dueño: ",
            self._propietario_service.buscar_propietarios_por_nombre,
        )
        self._imprimir_resultados(resultados)

    @staticmethod
    def _imprimir_resultados(resultados: Iterable[object]) -> None:
        resultados = list(resultados)
        if not resultados:
            print("No se encontraron resultados.")
            return
        for resultado in resultados:
            print("-" * 40)
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
