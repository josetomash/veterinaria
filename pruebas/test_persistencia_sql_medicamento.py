import sqlite3

from dao import MedicamentoDAO
from database import ConexionDB
from models import Medicamento


def main():
    print("==================================================")
    print("      PRUEBA DE PERSISTENCIA: MEDICAMENTO DAO")
    print("==================================================")

    lista_medicamentos = [
        Medicamento(999, "Amoxicilina 250mg", "Amoxicilina", "Antibiótico", 5500, 100),
        Medicamento(998, "Ketoprofeno 10mg", "Ketoprofeno", "Antiinflamatorio", 3200, 50),
        Medicamento(997, "Meloxicam 5mg", "Meloxicam", "Antiinflamatorio", 4500, 80),
    ]

    print("\n[1] Objetos creados en memoria RAM:")
    for indice, medicamento in enumerate(lista_medicamentos, start=1):
        print(f"\nObjeto [{indice}]:")
        print(f"    - ID: {medicamento.id_medicamento}")
        print(f"    - Nombre: {medicamento.nombre_comercial}")
        print(f"    - Precio: {medicamento.precio}")
        print(f"    - Stock: {medicamento.stock}")

    ruta_db = "database/clinica_vetcare.db"
    conexion = ConexionDB(ruta_db)
    dao = MedicamentoDAO(conexion)
    print(f"\n[2] DAO inicializado. Base de datos: {ruta_db}")

    print("\n[3] Enviando los objetos a la base de datos...")
    try:
        for medicamento in lista_medicamentos:
            dao.insertar(medicamento)
    except sqlite3.IntegrityError as error:
        print("\nNo se pudieron insertar todos los medicamentos.")
        print(f"Mensaje de error: {error}")
    else:
        print("\n¡ÉXITO TOTAL!")
        print(
            f"Se guardaron {len(lista_medicamentos)} medicamentos "
            f"en '{ruta_db}'."
        )

    print("\n==================================================")


if __name__ == "__main__":
    main()