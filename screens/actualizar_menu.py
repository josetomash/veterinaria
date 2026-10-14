import sqlite3

from models.consulta import Consulta
from models.detalle_consulta import DetalleConsulta
from models.especialidad import Especialidad
from models.especie import Especie
from models.mascota import Mascota
from models.medicamento import Medicamento
from models.propietario import Propietario
from models.receta_medica import RecetaMedica
from models.veterinario import Veterinario
from services.consulta_service import ConsultaService
from services.detalle_consulta_service import DetalleConsultaService
from services.mascota_service import MascotaService
from services.medicamento_service import MedicamentoService
from services.propietario_service import PropietarioService
from services.receta_medica_service import RecetaMedicaService
from services.veterinario_service import VeterinarioService
from screens.utilidades import (
    convertir_decimal,
    convertir_entero,
    convertir_fecha,
    convertir_si_no,
    elegir_de_lista,
    limpiar_pantalla,
    pausar,
    pedir_dato,
    validar,
)


class ActualizarMenu:
    def __init__(
        self,
        consulta_service: ConsultaService,
        detalle_consulta_service: DetalleConsultaService,
        mascota_service: MascotaService,
        medicamento_service: MedicamentoService,
        propietario_service: PropietarioService,
        receta_medica_service: RecetaMedicaService,
        veterinario_service: VeterinarioService,
    ):
        self._consulta_service = consulta_service
        self._detalle_consulta_service = detalle_consulta_service
        self._mascota_service = mascota_service
        self._medicamento_service = medicamento_service
        self._propietario_service = propietario_service
        self._receta_medica_service = receta_medica_service
        self._veterinario_service = veterinario_service

    def ejecutar(self):
        while True:
            limpiar_pantalla()
            print("\n=== Menú Actualizar ===")
            print("1. Actualizar consulta")
            print("2. Actualizar detalle de consulta")
            print("3. Actualizar mascota")
            print("4. Actualizar medicamento")
            print("5. Actualizar propietario")
            print("6. Actualizar receta médica")
            print("7. Actualizar veterinario")
            print("8. Volver al menú principal")
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self._ejecutar_actualizacion("consulta", self._actualizar_consulta)
            elif opcion == "2":
                self._ejecutar_actualizacion(
                    "detalle de consulta",
                    self._actualizar_detalle_consulta,
                )
            elif opcion == "3":
                self._ejecutar_actualizacion("mascota", self._actualizar_mascota)
            elif opcion == "4":
                self._ejecutar_actualizacion("medicamento", self._actualizar_medicamento)
            elif opcion == "5":
                self._ejecutar_actualizacion("propietario", self._actualizar_propietario)
            elif opcion == "6":
                self._ejecutar_actualizacion(
                    "receta médica",
                    self._actualizar_receta_medica,
                )
            elif opcion == "7":
                self._ejecutar_actualizacion("veterinario", self._actualizar_veterinario)
            elif opcion == "8":
                return
            else:
                print("Opción inválida. Intente nuevamente.")
                pausar()

    def _ejecutar_actualizacion(self, entidad, actualizar):
        try:
            actualizar()
        except (TypeError, ValueError, sqlite3.IntegrityError) as error:
            print(f"No se pudo actualizar {entidad}: {error}")
        else:
            print(f"{entidad.capitalize()} actualizado correctamente.")
        pausar()

    def _actualizar_consulta(self):
        consulta_actual = pedir_dato(
            "ID de la consulta a actualizar: ",
            lambda texto: self._consulta_service.obtener_consulta_por_id(convertir_entero(texto)),
        )
        motivo = pedir_dato(
            "Motivo: ",
            lambda texto: validar(Consulta, "motivo", texto.strip()),
        )
        fecha = pedir_dato(
            "Fecha (AAAA-MM-DD): ",
            lambda texto: validar(Consulta, "fecha_consulta", convertir_fecha(texto)),
        )
        id_veterinario = pedir_dato(
            "ID del veterinario: ",
            lambda texto: self._veterinario_service.obtener_veterinario_por_id(
                convertir_entero(texto)
            ).id_veterinario,
        )
        mascota = pedir_dato(
            "ID de la mascota: ",
            lambda texto: self._mascota_service.obtener_mascota_por_id(convertir_entero(texto)),
        )
        id_propietario = pedir_dato(
            "ID del propietario: ",
            lambda texto: self._propietario_de_mascota(convertir_entero(texto), mascota),
        )
        consulta = Consulta(
            consulta_actual.id_consulta,
            motivo,
            fecha,
            id_veterinario,
            mascota.id_mascota,
            id_propietario,
        )
        self._consulta_service.actualizar_consulta(consulta)

    def _propietario_de_mascota(self, id_propietario, mascota):
        """Comprueba que el propietario exista y que la mascota sea suya."""
        propietario = self._propietario_service.obtener_propietario_por_id(id_propietario)
        if mascota.id_propietario != propietario.id_propietario:
            raise ValueError(
                f"La mascota '{mascota.nombre}' no pertenece al propietario {propietario.nombre}."
            )
        return propietario.id_propietario

    def _actualizar_detalle_consulta(self):
        detalle_actual = pedir_dato(
            "ID del detalle de consulta a actualizar: ",
            lambda texto: self._detalle_consulta_service.obtener_detalle_consulta_por_id(
                convertir_entero(texto)
            ),
        )
        diagnostico = pedir_dato(
            "Diagnóstico: ",
            lambda texto: validar(DetalleConsulta, "diagnostico", texto.strip()),
        )
        tratamiento = pedir_dato(
            "Tratamiento: ",
            lambda texto: validar(DetalleConsulta, "tratamiento", texto.strip()),
        )
        receta = pedir_dato(
            "ID de la receta médica asociada: ",
            lambda texto: self._receta_medica_service.obtener_receta_medica_por_id(
                convertir_entero(texto)
            ),
        )
        id_consulta = pedir_dato(
            "ID de la consulta asociada: ",
            lambda texto: self._consulta_service.obtener_consulta_por_id(
                convertir_entero(texto)
            ).id_consulta,
        )
        detalle = DetalleConsulta(
            detalle_actual.id_detalle, diagnostico, tratamiento, receta, id_consulta
        )
        self._detalle_consulta_service.actualizar_detalle_consulta(detalle)

    def _actualizar_mascota(self):
        mascota_actual = pedir_dato(
            "ID de la mascota a actualizar: ",
            lambda texto: self._mascota_service.obtener_mascota_por_id(convertir_entero(texto)),
        )
        mascota = self._crear_mascota(mascota_actual.id_mascota, mascota_actual.id_propietario)
        self._mascota_service.actualizar_mascota(mascota)

    def _actualizar_medicamento(self):
        medicamento_actual = pedir_dato(
            "ID del medicamento a actualizar: ",
            lambda texto: self._medicamento_service.obtener_medicamento_por_id(
                convertir_entero(texto)
            ),
        )
        medicamento = Medicamento(
            medicamento_actual.id_medicamento,
            pedir_dato(
                "Nombre comercial: ",
                lambda texto: validar(Medicamento, "nombre_comercial", texto.strip()),
            ),
            pedir_dato(
                "Nombre genérico: ",
                lambda texto: validar(Medicamento, "nombre_generico", texto.strip()),
            ),
            pedir_dato(
                "Tipo: ",
                lambda texto: validar(Medicamento, "tipo", texto.strip()),
            ),
            pedir_dato(
                "Precio: ",
                lambda texto: validar(Medicamento, "precio", convertir_decimal(texto)),
            ),
            pedir_dato(
                "Stock: ",
                lambda texto: validar(Medicamento, "stock", convertir_entero(texto)),
            ),
        )
        self._medicamento_service.actualizar_medicamento(medicamento)

    def _actualizar_propietario(self):
        propietario_actual = pedir_dato(
            "ID del propietario a actualizar: ",
            lambda texto: self._propietario_service.obtener_propietario_por_id(
                convertir_entero(texto)
            ),
        )
        id_propietario = propietario_actual.id_propietario
        nombre = pedir_dato(
            "Nombre: ",
            lambda texto: validar(Propietario, "nombre", texto.strip()),
        )
        rut = pedir_dato(
            "RUT: ",
            lambda texto: self._rut_disponible(
                texto,
                Propietario,
                self._propietario_service.obtener_propietario_por_rut,
                lambda otro: otro.id_propietario == id_propietario,
                "propietario",
            ),
        )
        telefono = pedir_dato(
            "Teléfono (+569...): ",
            lambda texto: validar(Propietario, "telefono", texto.strip()),
        )
        email = pedir_dato(
            "Correo electrónico: ",
            lambda texto: validar(Propietario, "email", texto.strip()),
        )

        propietario = Propietario(
            nombre,
            rut,
            telefono,
            id_propietario,
            email,
            propietario_actual.mascotas,
        )

        # Primero se piden todos los datos y recién al final se guarda,
        # así si el usuario se equivoca 3 veces no queda nada a medias.
        mascota_actualizada = None
        if propietario_actual.mascotas:
            actualizar_mascota = pedir_dato(
                "¿Desea actualizar también una de sus mascotas? (S/N): ",
                convertir_si_no,
            )
            if actualizar_mascota:
                print("Mascotas del propietario:")
                for indice, opcion in enumerate(propietario_actual.mascotas, start=1):
                    print(f"{indice}. {opcion.nombre} ({opcion.tipo_especie})")
                mascota = elegir_de_lista(
                    "Seleccione la mascota: ", propietario_actual.mascotas, "mascota"
                )
                mascota_actualizada = self._crear_mascota(mascota.id_mascota, id_propietario)

        self._propietario_service.actualizar_propietario(propietario)
        if mascota_actualizada is not None:
            self._mascota_service.actualizar_mascota(mascota_actualizada)

    @staticmethod
    def _rut_disponible(texto, clase, obtener_por_rut, es_el_mismo, entidad):
        """Valida el RUT y revisa que no lo use otro registro distinto al que se actualiza."""
        rut = validar(clase, "rut", texto.strip())
        try:
            otro = obtener_por_rut(rut)
        except ValueError:
            return rut
        if not es_el_mismo(otro):
            raise ValueError(f"Ya existe otro {entidad} con ese RUT.")
        return rut

    def _crear_mascota(self, id_mascota, id_propietario=None):
        nombre = pedir_dato(
            "Nombre de mascota: ",
            lambda texto: validar(Mascota, "nombre", texto.strip()),
        )
        fecha_nacimiento = pedir_dato(
            "Fecha de nacimiento (AAAA-MM-DD): ",
            lambda texto: validar(Mascota, "fecha_nacimiento", convertir_fecha(texto)),
        )
        especies = list(Especie)
        print("Especies:")
        for indice, especie in enumerate(especies, start=1):
            print(f"{indice}. {especie.nombre_especie}")
        especie = elegir_de_lista("Seleccione una especie: ", especies, "especie")
        return Mascota(
            id_mascota,
            nombre,
            fecha_nacimiento,
            especie,
            id_propietario,
        )

    def _actualizar_receta_medica(self):
        receta_actual = pedir_dato(
            "ID de la receta médica a actualizar: ",
            lambda texto: self._receta_medica_service.obtener_receta_medica_por_id(
                convertir_entero(texto)
            ),
        )
        receta = RecetaMedica(
            receta_actual.id_receta,
            pedir_dato(
                "Nombre comercial: ",
                lambda texto: validar(RecetaMedica, "nombre_comercial", texto.strip()),
            ),
            pedir_dato(
                "Cantidad en mg: ",
                lambda texto: validar(RecetaMedica, "cantidad_mg", convertir_entero(texto)),
            ),
            pedir_dato(
                "Instrucciones: ",
                lambda texto: validar(RecetaMedica, "instrucciones", texto.strip()),
            ),
        )
        self._receta_medica_service.actualizar_receta_medica(receta)

    def _actualizar_veterinario(self):
        veterinario_actual = pedir_dato(
            "ID del veterinario a actualizar: ",
            lambda texto: self._veterinario_service.obtener_veterinario_por_id(
                convertir_entero(texto)
            ),
        )
        id_veterinario = veterinario_actual.id_veterinario
        nombre = pedir_dato(
            "Nombre: ",
            lambda texto: validar(Veterinario, "nombre", texto.strip()),
        )
        rut = pedir_dato(
            "RUT: ",
            lambda texto: self._rut_disponible(
                texto,
                Veterinario,
                self._veterinario_service.obtener_veterinario_por_rut,
                lambda otro: otro.id_veterinario == id_veterinario,
                "veterinario",
            ),
        )
        telefono = pedir_dato(
            "Teléfono (+569...): ",
            lambda texto: validar(Veterinario, "telefono", texto.strip()),
        )
        especialidades = list(Especialidad)
        print("Especialidades:")
        for indice, especialidad in enumerate(especialidades, start=1):
            print(f"{indice}. {especialidad.value}")
        especialidad = elegir_de_lista(
            "Seleccione una especialidad: ", especialidades, "especialidad"
        )

        veterinario = Veterinario(
            id_veterinario,
            nombre,
            rut,
            telefono,
            especialidad,
        )
        self._veterinario_service.actualizar_veterinario(veterinario)
