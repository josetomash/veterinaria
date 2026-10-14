from models.consulta import Consulta
from models.especie import Especie
from models.especialidad import Especialidad
from models.detalle_consulta import DetalleConsulta
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


class RegistrarMenu:
    def __init__(
        self,
        propietario_service: PropietarioService,
        mascota_service: MascotaService,
        veterinario_service: VeterinarioService,
        medicamento_service: MedicamentoService,
        receta_medica_service: RecetaMedicaService,
        detalle_consulta_service: DetalleConsultaService,
        consulta_service: ConsultaService,
    ):
        self._propietario_service = propietario_service
        self._mascota_service = mascota_service
        self._veterinario_service = veterinario_service
        self._medicamento_service = medicamento_service
        self._receta_medica_service = receta_medica_service
        self._detalle_consulta_service = detalle_consulta_service
        self._consulta_service = consulta_service

    def mostrar_menu(self):
        print("=== Menú de Registro ===")
        print("Bienvenido al sistema de gestión veterinaria")
        print("1. Asignar Propietario")
        print("2. Asignar Mascota")
        print("3. Asignar Veterinario")
        print("4. Registrar Medicamento")
        print("5. Registrar Receta Médica")
        print("6. Registrar Detalle de Consulta")
        print("7. Registrar Consulta")
        print("8. Salir")
        print("======================")
        return input("Seleccione una opción: ").strip()

    def ejecutar(self):
        while True:
            limpiar_pantalla()
            opcion = self.mostrar_menu()
            if opcion == "1":
                respuesta = input("¿Desea registrar un propietario? (S/N): ").strip()
                if respuesta.lower() == "s":
                    self._registrar_propietario()
            elif opcion == "2":
                self._registrar_mascota()
            elif opcion == "3":
                self._registrar_veterinario()
            elif opcion == "4":
                self._registrar_medicamento()
            elif opcion == "5":
                self._registrar_receta_medica()
            elif opcion == "6":
                self._registrar_detalle_consulta()
            elif opcion == "7":
                self._registrar_consulta()
            elif opcion == "8":
                print("Saliendo del menú de registro...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")
                pausar()

    def _registrar_propietario(self):
        try:
            propietario = self._crear_propietario()
            self._propietario_service.registrar_propietario(propietario)
            print(f"[OK] Registro de propietario exitoso. ID asignado: {propietario.id_propietario}")
            for mascota in propietario.mascotas:
                print(f"     Mascota '{mascota.nombre}' registrada con ID: {mascota.id_mascota}")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
        pausar()

    def _registrar_mascota(self):
        try:
            # Toda mascota debe tener dueño: uno ya registrado o uno nuevo
            print("¿A quién pertenece la mascota?")
            print("1. A un dueño ya registrado")
            print("2. A un dueño nuevo (registrarlo ahora)")
            opcion = elegir_de_lista("Seleccione una opción: ", ["existente", "nuevo"], "opción")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
            pausar()
            return
        if opcion == "nuevo":
            # Registra al dueño junto con su mascota
            self._registrar_propietario()
            return
        try:
            propietario = pedir_dato(
                "RUT del dueño: ",
                self._propietario_service.obtener_propietario_por_rut,
            )
            print(f"Dueño: {propietario.nombre}")
            mascota = self._crear_mascota(propietario.id_propietario)
            self._mascota_service.registrar_mascota(mascota)
            print(f"[OK] Registro de mascota exitoso. ID asignado: {mascota.id_mascota}")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
        pausar()

    def _registrar_veterinario(self):
        try:
            veterinario = self._crear_veterinario()
            self._veterinario_service.registrar_veterinario(veterinario)
            print(f"[OK] Registro de veterinario exitoso. ID asignado: {veterinario.id_veterinario}")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
        pausar()

    def _registrar_medicamento(self):
        try:
            medicamento = self._crear_medicamento()
            self._medicamento_service.registrar_medicamento(medicamento)
            print(f"[OK] Registro de medicamento exitoso. ID asignado: {medicamento.id_medicamento}")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
        pausar()

    def _registrar_receta_medica(self):
        try:
            receta = self._crear_receta_medica()
            self._receta_medica_service.registrar_receta_medica(receta)
            print(f"[OK] Registro de receta médica exitoso. ID asignado: {receta.id_receta}")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
        pausar()

    def _registrar_detalle_consulta(self):
        try:
            detalle = self._crear_detalle_consulta()
            self._detalle_consulta_service.registrar_detalle_consulta(detalle)
            print(f"[OK] Registro de detalle de consulta exitoso. ID asignado: {detalle.id_detalle}")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
        pausar()

    def _registrar_consulta(self):
        try:
            consulta = self._crear_consulta()
            self._consulta_service.registrar_consulta(consulta)
            print(f"[OK] Registro de consulta exitoso. ID asignado: {consulta.id_consulta}")
        except (ValueError, TypeError) as error:
            print(f"\n[Error de registro] {error}")
        pausar()

    def _crear_mascota(self, id_propietario=None) -> Mascota:
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
            None,  # el ID lo asigna la base de datos
            nombre,
            fecha_nacimiento,
            especie,
            id_propietario,
        )

    def _rut_propietario_disponible(self, texto: str) -> str:
        rut = validar(Propietario, "rut", texto.strip())
        try:
            self._propietario_service.obtener_propietario_por_rut(rut)
        except ValueError:
            return rut  # no existe: se puede usar
        raise ValueError("Ya existe un propietario con ese RUT.")

    def _crear_propietario(self) -> Propietario:
        nombre = pedir_dato(
            "Nombre del propietario: ",
            lambda texto: validar(Propietario, "nombre", texto.strip()),
        )
        rut = pedir_dato("RUT: ", self._rut_propietario_disponible)
        telefono = pedir_dato(
            "Teléfono (+569...): ",
            lambda texto: validar(Propietario, "telefono", texto.strip()),
        )
        email = pedir_dato(
            "Correo electrónico: ",
            lambda texto: validar(Propietario, "email", texto.strip()),
        )
        # Un propietario puede tener varias mascotas
        print("\n--- Datos de la mascota ---")
        mascotas = [self._crear_mascota()]
        while pedir_dato("¿Desea agregar otra mascota? (S/N): ", convertir_si_no):
            print("\n--- Datos de la mascota ---")
            mascotas.append(self._crear_mascota())
        return Propietario(
            nombre=nombre,
            rut=rut,
            telefono=telefono,
            id_propietario=None,  # el ID lo asigna la base de datos
            email=email,
            mascotas=mascotas,
        )

    def _rut_veterinario_disponible(self, texto: str) -> str:
        rut = validar(Veterinario, "rut", texto.strip())
        try:
            self._veterinario_service.obtener_veterinario_por_rut(rut)
        except ValueError:
            return rut  # no existe: se puede usar
        raise ValueError("Ya existe un veterinario con ese RUT.")

    def _crear_veterinario(self) -> Veterinario:
        nombre = pedir_dato(
            "Nombre del veterinario: ",
            lambda texto: validar(Veterinario, "nombre", texto.strip()),
        )
        rut = pedir_dato("RUT: ", self._rut_veterinario_disponible)
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
        return Veterinario(
            None,  # el ID lo asigna la base de datos
            nombre,
            rut,
            telefono,
            especialidad,
        )

    def _crear_medicamento(self) -> Medicamento:
        return Medicamento(
            None,  # el ID lo asigna la base de datos
            pedir_dato(
                "Nombre comercial: ",
                lambda texto: validar(Medicamento, "nombre_comercial", texto.strip()),
            ),
            pedir_dato(
                "Nombre genérico: ",
                lambda texto: validar(Medicamento, "nombre_generico", texto.strip()),
            ),
            pedir_dato(
                "Tipo de medicamento: ",
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

    def _crear_receta_medica(self) -> RecetaMedica:
        return RecetaMedica(
            None,  # el ID lo asigna la base de datos
            pedir_dato(
                "Nombre comercial del medicamento: ",
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

    def _crear_detalle_consulta(self) -> DetalleConsulta:
        receta = pedir_dato(
            "ID de la receta médica: ",
            lambda texto: self._receta_medica_service.obtener_receta_medica_por_id(
                convertir_entero(texto)
            ),
        )
        consulta = pedir_dato(
            "ID de la consulta a la que pertenece el detalle: ",
            lambda texto: self._consulta_service.obtener_consulta_por_id(
                convertir_entero(texto)
            ),
        )
        return DetalleConsulta(
            None,  # el ID lo asigna la base de datos
            pedir_dato(
                "Diagnóstico: ",
                lambda texto: validar(DetalleConsulta, "diagnostico", texto.strip()),
            ),
            pedir_dato(
                "Tratamiento: ",
                lambda texto: validar(DetalleConsulta, "tratamiento", texto.strip()),
            ),
            receta,
            consulta.id_consulta,
        )

    def _crear_consulta(self) -> Consulta:
        propietario = pedir_dato(
            "RUT del propietario: ",
            self._propietario_service.obtener_propietario_por_rut,
        )
        if not propietario.mascotas:
            raise ValueError("El propietario no tiene mascotas registradas.")
        if len(propietario.mascotas) == 1:
            mascota = propietario.mascotas[0]
            print(f"Mascota del propietario: {mascota.nombre}")
        else:
            print("Mascotas del propietario:")
            for indice, opcion in enumerate(propietario.mascotas, start=1):
                print(f"{indice}. {opcion.nombre} ({opcion.tipo_especie})")
            mascota = elegir_de_lista(
                "Seleccione la mascota: ", propietario.mascotas, "mascota"
            )
        veterinario = pedir_dato(
            "RUT del veterinario: ",
            self._veterinario_service.obtener_veterinario_por_rut,
        )
        return Consulta(
            None,  # el ID lo asigna la base de datos
            pedir_dato(
                "Motivo: ",
                lambda texto: validar(Consulta, "motivo", texto.strip()),
            ),
            pedir_dato(
                "Fecha (AAAA-MM-DD): ",
                lambda texto: validar(Consulta, "fecha_consulta", convertir_fecha(texto)),
            ),
            veterinario.id_veterinario,
            mascota.id_mascota,
            propietario.id_propietario,
        )
