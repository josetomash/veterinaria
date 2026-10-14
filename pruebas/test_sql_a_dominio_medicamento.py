from dao import MedicamentoDAO
from database import ConexionDB
from models import Medicamento


def main():
    conexion = ConexionDB()
    dao = MedicamentoDAO(conexion)

    print("=== INICIO DE PRUEBAS DE DOMINIO ===")

    try:
        medicamento = dao.obtener_por_id_estricto(1)
        print(f"Tipo de objeto: {type(medicamento)}")
        print(
            f"Fármaco: {medicamento.nombre_comercial} | "
            f"Precio: ${medicamento.precio} | Stock: {medicamento.stock}"
        )

        medicamento.stock -= 10
        print(f"Stock tras descuento en el objeto: {medicamento.stock}")
    except ValueError as error:
        print(f"[ENTIDAD NO ENCONTRADA]: {error}")

    try:
        medicamento_inexistente = dao.obtener_por_id_estricto(999)
        print(f"Resultado ID inexistente: {medicamento_inexistente}")
    except ValueError as error:
        print(f"[ENTIDAD NO ENCONTRADA]: {error}")

    medicamentos = dao.listar_todos()
    print("\n==================================================")
    print("Listado completo de medicamentos en la base de datos:")
    print("==================================================")
    if not medicamentos:
        print("La base de datos no contiene registros.")
    else:
        for indice, medicamento in enumerate(medicamentos, start=1):
            print(
                f" [{indice:03d}] Nombre: {medicamento.nombre_comercial:<20} | "
                f"Precio: ${medicamento.precio:<8} | Stock: {medicamento.stock}"
            )


if __name__ == "__main__":
    main()
