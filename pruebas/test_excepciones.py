import sqlite3

from database.conexion import ConexionDB
from dao.medicamento_dao import MedicamentoDAO
from models.medicamento import Medicamento

#la capa DAO maneja exactamente los errores esperados,
#la base de datos y las reglas de FK se respetan,
#el modelo de dominio rechaza datos inválidos.

def ejecutar_suite_pruebas():
    conexion = ConexionDB()
    dao = MedicamentoDAO(conexion)

    print("=" * 65)
    print("SUITE DE EXCEPCIONES — MEDICAMENTODAO")
    print("=" * 65)

    id_inexistente = 99999
    while True:
        try:
            dao.obtener_por_id_estricto(id_inexistente)
            id_inexistente += 1
        except ValueError:
            break

    print(
        f"\n[TEST 1] Buscando medicamento inexistente #{id_inexistente}..."
    )
    try:
        dao.obtener_por_id_estricto(id_inexistente)
    except ValueError as error:
        print(f" -> Aprobado. Capturado: {error}")
    else:
        raise AssertionError("No se lanzó ValueError para un ID inexistente.")

    id_prueba = id_inexistente + 1
    while True:
        try:
            dao.obtener_por_id_estricto(id_prueba)
            id_prueba += 1
        except ValueError:
            break

    medicamento_prueba = Medicamento(
        id_prueba,
        f"Medicamento prueba {id_prueba}",
        "Genérico de prueba",
        "Prueba",
        1000,
        10,
    )
    dao.insertar(medicamento_prueba)

    print(f"\n[TEST 2] Intentando insertar ID duplicado #{id_prueba}...")
    try:
        dao.insertar(medicamento_prueba)
    except sqlite3.IntegrityError as error:
        print(f" -> Aprobado. Capturado: {error}")
    else:
        raise AssertionError("No se lanzó IntegrityError para un ID duplicado.")
    finally:
        dao.eliminar(id_prueba)

    print("\n[TEST 3] Verificando rechazo de un precio negativo...")
    try:
        Medicamento(
            15,
            "Fármaco de prueba",
            "Genérico de prueba",
            "Prueba",
            -500,
            10,
        )
    except ValueError as error:
        print(f" -> Aprobado. Invariante protegió el modelo: {error}")
    else:
        raise AssertionError("El modelo permitió asignar un precio negativo.")

    print("\n" + "=" * 65)
    print("[ÉXITO] TODAS LAS PRUEBAS PASARON")
    print("=" * 65)


if __name__ == "__main__":
    ejecutar_suite_pruebas()