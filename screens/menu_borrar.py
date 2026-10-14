import sqlite3

from services.consulta_service import ConsultaService
from services.detalle_consulta_service import DetalleConsultaService
from services.especie_service import EspecieService
from services.mascota_service import MascotaService
from services.medicamento_service import MedicamentoService
from services.propietario_service import PropietarioService
from services.receta_medica_service import RecetaMedicaService
from services.veterinario_service import VeterinarioService
from screens.utilidades import (
    DemasiadosIntentos,
    convertir_entero,
    limpiar_pantalla,
    pausar,
    pedir_dato,
)


class MenuBorrar:
    def __init__(
        self,
        consulta_service: ConsultaService,
        propietario_service: PropietarioService,
        mascota_service: MascotaService,
        veterinario_service: VeterinarioService,
        detalle_consulta_service: DetalleConsultaService,
        medicamento_service: MedicamentoService,
        receta_medica_service: RecetaMedicaService,
    ):
        self._consulta_service = consulta_service
        self._propietario_service = propietario_service
        self._mascota_service = mascota_service
        self._veterinario_service = veterinario_service
        self._detalle_consulta_service = detalle_consulta_service
        self._medicamento_service = medicamento_service
        self._receta_medica_service = receta_medica_service

    def ejecutar(self) -> None:
        while True:
            limpiar_pantalla()
            print("\n=== Menú Borrar ===")
            print("1. Borrar consulta")
            print("2. Borrar propietario")
            print("3. Borrar mascota")
            print("4. Borrar veterinario")
            print("5. Borrar detalle de consulta")
            print("6. Borrar medicamento")
            print("7. Borrar receta médica")
            print("8. Volver al menú principal")
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                Y=input("Esta seguro que desea borrar el registro? (S/N): ").strip().upper()
                if Y == "S":
                    self.borrar_consulta()
            elif opcion == "2":
                Y=input("Esta seguro que desea borrar el registro? (S/N): ").strip().upper()
                if Y == "S":
                    self.borrar_propietario()
            elif opcion == "3":
                Y=input("Esta seguro que desea borrar el registro? (S/N): ").strip().upper()
                if Y == "S":
                    self.borrar_mascota()
            elif opcion == "4":
                Y=input("Esta seguro que desea borrar el registro? (S/N): ").strip().upper()
                if Y == "S":
                    self.borrar_veterinario()
            elif opcion == "5":
                Y=input("Esta seguro que desea borrar el registro? (S/N): ").strip().upper()
                if Y == "S":
                    self.borrar_detalle_consulta()
            elif opcion == "6":
                Y=input("Esta seguro que desea borrar el registro? (S/N): ").strip().upper()
                if Y == "S":
                    self.borrar_medicamento()
            elif opcion == "7":
                Y=input("Esta seguro que desea borrar el registro? (S/N): ").strip().upper()
                if Y == "S":
                    self.borrar_receta_medica()
            elif opcion == "8":
                return
            else:
                print("Opción inválida. Intente nuevamente.")
            pausar()

    def _borrar_por_id(self, entidad, accion):
        try:
            id_registro = pedir_dato(
                f"Ingrese el ID de {entidad} a borrar: ",
                self._convertir_id,
            )
        except DemasiadosIntentos as error:
            print(f"No se pudo borrar el registro: {error}")
            return

        try:
            accion(id_registro)
        except (TypeError, ValueError) as error:
            print(f"No se pudo borrar el registro de {entidad}: {error}")
            return
        except sqlite3.IntegrityError:
            print(
                f"No se pudo borrar el registro de {entidad}: existen registros relacionados "
                "que impiden la eliminación."
            )
            return

        print(f"El registro de {entidad} se eliminó correctamente.")

    @staticmethod
    def _convertir_id(texto: str) -> int:
        id_registro = convertir_entero(texto)
        if id_registro <= 0:
            raise ValueError("El ID debe ser un número entero positivo.")
        return id_registro

    def borrar_consulta(self) -> None:
        self._borrar_por_id("consulta", self._consulta_service.borrar_consulta)

    def borrar_propietario(self) -> None:
        self._borrar_por_id("propietario", self._propietario_service.borrar_propietario)

    def borrar_mascota(self) -> None:
        self._borrar_por_id("mascota", self._mascota_service.borrar_mascota)

    def borrar_veterinario(self) -> None:
        self._borrar_por_id("veterinario", self._veterinario_service.borrar_veterinario)

    def borrar_detalle_consulta(self) -> None:
        self._borrar_por_id(
            "detalle de consulta",
            self._detalle_consulta_service.borrar_detalle_consulta,
        )

    def borrar_medicamento(self) -> None:
        self._borrar_por_id("medicamento", self._medicamento_service.borrar_medicamento)

    def borrar_receta_medica(self) -> None:
        self._borrar_por_id("receta médica", self._receta_medica_service.borrar_receta_medica)
