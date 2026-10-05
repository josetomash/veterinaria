from datetime import date
import os
from models.especie import Especie
from models.propietario import Propietario
from models.mascota import Mascota
from services.clinica_service import ClinicaService

class RegistrarMenu:
    def __init__(self, clinica_service: ClinicaService):
        self._clinica_service = clinica_service

    def mostrar_menu(self):
        print("=== Menú de Registro ===")
        print("Bienvenido al sistema de gestión veterinaria")
        print("1. Asignar Propietario")
        print("2. Asignar Mascota")
        print("3. Asignar Veterinario")
        print("4. Salir")
        print("======================")
        return input("Seleccione una opción: ").strip()

    def ejecutar(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            opcion = self.mostrar_menu()
            # propietario
            if opcion == "1":
                respuesta = input("¿Desea registrar un propietario? (S/N): ").strip()
                if respuesta.lower() == "s":

                    # HASTA EL MOMENTO ESTO ES UN MOCK PARA SABER SI ESTA BIEN.
                    try:
                        nueva_mascota = Mascota(
                            id_mascota=1,
                            nombre="Firulais",
                            fecha_nacimiento=date(2020, 1, 1),
                            especie=Especie.CANINO,
                        )
                        nuevo_propietario = Propietario(
                                nombre="Juan Perez",
                                rut="11222333-9",
                                telefono="+56912345678",
                                id_propietario=99,
                                email="juan.perez@email.com",
                                mascota=nueva_mascota 
                            )
                            
                        self._clinica_service.registrar_propietario(nuevo_propietario)                       
                    except ValueError as e:
                        print(f"\n[Error de validación] {e}")
                        input("Presione Enter para reintentar...")
                        continue
                    except TypeError as e:
                        print(f"\n[Error de tipo] {e}")
                        input("Presione Enter para reintentar...")
                        continue

            # mascota
            elif opcion == "2":
                self._clinica_service.registrar_mascota()
            # veterinario
            elif opcion == "3":
                self._clinica_service.registrar_veterinario()
            elif opcion == "4":
                print("Saliendo del menú de registro...")
                break
            else:
                print("Opción no válida. Intente nuevamente.")